import re
from datetime import datetime

import feedparser
import pytz
import requests
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce
from bravado.exception import HTTPBadGateway, HTTPGatewayTimeout, HTTPServiceUnavailable
from celery import shared_task
from django.utils.html import strip_tags
from ics import Calendar
from requests.exceptions import RequestException

from .app_settings import (
    OPCALENDAR_CAS_URL,
    OPCALENDAR_EVE_LINKNET_URL,
    OPCALENDAR_EVE_UNI_URL,
    OPCALENDAR_FREE_RANGE_CHIKUNS_URL,
    OPCALENDAR_FRIDAY_YARRRR_URL,
    OPCALENDAR_FUNINC_URL,
    OPCALENDAR_FWAMING_DWAGONS_URL,
    OPCALENDAR_REDEMPTION_ROAD_URL,
    OPCALENDAR_SPECTRE_URL,
    OPCALENDAR_TASKS_TIME_LIMIT,
)
from .models import Event, EventImport, Owner

DEFAULT_TASK_PRIORITY = 6

logger = get_extension_logger(__name__)

# Create your tasks here
TASK_DEFAULT_KWARGS = {
    "time_limit": OPCALENDAR_TASKS_TIME_LIMIT,
}

TASK_ESI_KWARGS = {
    **TASK_DEFAULT_KWARGS,
    **{
        "bind": True,
        "autoretry_for": (
            OSError,
            HTTPBadGateway,
            HTTPGatewayTimeout,
            HTTPServiceUnavailable,
        ),
        "retry_kwargs": {"max_retries": 3},
        "retry_backoff": 30,
    },
}


@shared_task
def import_all_npsi_fleets() -> bool:
    """Imports all NPSI fleets from their respective APIs"""

    # Get all current imported fleets in database
    event_ids_to_remove = set(
        Event.objects.filter(external=True).values_list("id", flat=True)
    )

    logger.debug("External events in database: {}".format(event_ids_to_remove))

    # Get all import feeds
    feeds = EventImport.objects.all()

    feed_errors = []
    map_ical_imports = {
        EventImport.FRIDAY_YARRRR: OPCALENDAR_FRIDAY_YARRRR_URL,
        EventImport.REDEMPTION_ROAD: OPCALENDAR_REDEMPTION_ROAD_URL,
        EventImport.CAS: OPCALENDAR_CAS_URL,
        EventImport.FREE_RANGE_CHIKUNS: OPCALENDAR_FREE_RANGE_CHIKUNS_URL,
        EventImport.EVE_LINKNET: OPCALENDAR_EVE_LINKNET_URL,
        EventImport.FWAMING_DWAGONS: OPCALENDAR_FWAMING_DWAGONS_URL,
    }

    # Check for active NPSI feeds
    for feed in feeds:
        # If Spectre Fleet is active
        if feed.source == EventImport.SPECTRE_FLEET:
            has_error = _import_spectre_fleet(feed, event_ids_to_remove)
            feed_errors.append(has_error)

        # Check for FUN Inc fleets
        if feed.source == EventImport.FUN_INC:
            has_error = _import_fun_inc(feed, event_ids_to_remove)
            feed_errors.append(has_error)

        # Check for EVE Uni events
        if feed.source == EventImport.EVE_UNIVERSITY:
            has_error = _import_eve_uni(feed, event_ids_to_remove)
            feed_errors.append(has_error)

        # Check for events from ical feeds
        for source, url in map_ical_imports.items():
            if feed.source == source:
                has_error = _import_ical(feed, event_ids_to_remove, url)
                feed_errors.append(has_error)

    logger.debug("Checking for NPSI fleets to be removed.")

    successful_imports = feed_errors.count(False)
    if successful_imports:
        logger.info(
            "Successfully imported %d / %d NPSI feeds.",
            successful_imports,
            len(feed_errors),
        )

    if any(feed_errors):
        logger.error("Errors in feeds, not cleaning up operations on this run")
        return False

    if not event_ids_to_remove:
        logger.debug("No NPSI fleets to be removed.")
    else:
        logger.debug("Removed unseen NPSI fleets")
        # Remove all events we did not see from API
        Event.objects.filter(pk__in=event_ids_to_remove).delete()
    return True


def _import_spectre_fleet(feed, event_ids_to_remove):
    logger.debug(
        "%s: import feed active. Pulling events from %s",
        feed,
        OPCALENDAR_SPECTRE_URL,
    )

    try:
        # Get spectre fleets from their RSS feed
        d = feedparser.parse(OPCALENDAR_SPECTRE_URL)

        # Process each fleet entry
        for entry in d.entries:
            # Look for SF fleets only
            if entry.author_detail.name == "Spectre Fleet":
                # Only active fleets
                if "[RESERVED]" not in entry.title:
                    logger.debug("%s: Import even found: %s", feed, entry.title)

                    # Format datetimes
                    date_object = datetime.strptime(
                        entry.published, "%a, %d %b %Y %H:%M:%S %z"
                    )
                    date_object.strftime("%Y-%m-%dT%H:%M")

                    # Check if we already have the event stored
                    original = Event.objects.filter(
                        start_time=date_object, title=entry.title
                    ).first()

                    # If we get the event from API it should not be removed
                    if original:
                        logger.debug(
                            "%s: Event: %s already in database, skipping",
                            feed,
                            entry.title,
                        )

                        # Remove the found fleet from the to be removed list
                        event_ids_to_remove.discard(original.id)

                    else:
                        # Save new fleet to database
                        Event.objects.create(
                            operation_type=feed.operation_type,
                            title=entry.title,
                            host=feed.host,
                            doctrine="see details",
                            formup_system=feed.source,
                            description=strip_tags(entry.description),
                            start_time=date_object,
                            end_time=date_object,
                            fc=feed.source,
                            external=True,
                            user=feed.creator,
                            event_visibility=feed.event_visibility,
                            eve_character=feed.eve_character,
                        )

                        logger.debug(
                            "%s: Saved new event in database: %s",
                            feed,
                            entry.title,
                        )

    except (NotImplementedError, RequestException):
        logger.error("%s: Error in fetching fleets", feed, exc_info=True)
        return True

    return False


def _import_fun_inc(feed, event_ids_to_remove):
    logger.debug(
        "%s: import feed active. Pulling events from %s",
        feed,
        OPCALENDAR_FUNINC_URL,
    )

    try:
        # Get FUN Inc fleets from google ical
        r = requests.get(OPCALENDAR_FUNINC_URL)
        r.raise_for_status()

        c = Calendar(r.text)

        # Parse each entry we got
        for entry in c.events:
            # Format datetime
            start_date = datetime.utcfromtimestamp(entry.begin.float_timestamp).replace(
                tzinfo=pytz.utc
            )
            end_date = datetime.utcfromtimestamp(entry.end.float_timestamp).replace(
                tzinfo=pytz.utc
            )
            title = entry.name if entry.name else ""

            logger.debug("%s: Import even found: %s", feed, title)

            # Check if we already have the event stored
            original = Event.objects.filter(start_time=start_date, title=title).first()

            # If we get the event from API it should not be removed
            if original:
                logger.debug("%s: Event: %s already in database, skipping", feed, title)

                # Remove the found fleet from the to be removed list
                event_ids_to_remove.discard(original.id)

            else:
                # Save new fleet to database
                event = Event(
                    operation_type=feed.operation_type,
                    title=title,
                    host=feed.host,
                    doctrine="see details",
                    formup_system=feed.source,
                    description=strip_tags(entry.description),
                    start_time=start_date,
                    end_time=end_date,
                    fc=feed.source,
                    external=True,
                    user=feed.creator,
                    event_visibility=feed.event_visibility,
                    eve_character=feed.eve_character,
                )

                logger.debug("%s: Saved new EVE UNI event in database: %s", feed, title)

                event.save()

    except (NotImplementedError, RequestException):
        logger.error("%s: Error in fetching fleets", feed, exc_info=True)
        return True

    return False


def _import_eve_uni(feed, event_ids_to_remove):
    logger.debug(
        "%s: import feed active. Pulling events from %s",
        feed,
        OPCALENDAR_EVE_UNI_URL,
    )

    try:
        # Get EVE Uni events from their API feed (ical)
        r = requests.get(OPCALENDAR_EVE_UNI_URL)
        r.raise_for_status()

        c = Calendar(r.text)
        for entry in c.events:
            # Filter only class events as they are the only public events in eveuni
            if entry.name and "class" in entry.name.lower():
                # Format datetime
                start_date = datetime.utcfromtimestamp(
                    entry.begin.float_timestamp
                ).replace(tzinfo=pytz.utc)
                end_date = datetime.utcfromtimestamp(entry.end.float_timestamp).replace(
                    tzinfo=pytz.utc
                )
                title = re.sub(r"[\(\[].*?[\)\]]", "", entry.name)

                logger.debug("%s: Import even found: %s", feed, title)

                # Check if we already have the event stored
                original = Event.objects.filter(
                    start_time=start_date, title=title
                ).first()

                # If we get the event from API it should not be removed
                if original:
                    logger.debug(
                        "%s: Event: %s already in database, skipping", feed, title
                    )

                    # Remove the found fleet from the to be removed list
                    event_ids_to_remove.discard(original.id)

                else:
                    # Save new event to database
                    event = Event(
                        operation_type=feed.operation_type,
                        title=title,
                        host=feed.host,
                        doctrine="see details",
                        formup_system=feed.source,
                        description=strip_tags(entry.description.replace("<br>", "\n")),
                        start_time=start_date,
                        end_time=end_date,
                        fc=feed.source,
                        external=True,
                        user=feed.creator,
                        event_visibility=feed.event_visibility,
                        eve_character=feed.eve_character,
                    )

                    logger.debug(
                        "%s: Saved new EVE UNI event in database: %s",
                        feed,
                        title,
                    )
                    event.save()

    except (NotImplementedError, RequestException):
        logger.error("%s: Error in fetching fleets", feed, exc_info=True)
        return True

    return False


def _import_ical(feed, event_ids_to_remove, url):
    logger.debug(
        "%s: import feed active. Pulling events from %s",
        feed,
        url,
    )

    try:
        # Get EVE Uni events from their API feed (ical)
        r = requests.get(url)
        r.raise_for_status()

        c = Calendar(r.text)
        for entry in c.events:
            # Format datetime
            start_date = datetime.utcfromtimestamp(entry.begin.float_timestamp).replace(
                tzinfo=pytz.utc
            )
            end_date = datetime.utcfromtimestamp(entry.end.float_timestamp).replace(
                tzinfo=pytz.utc
            )
            title = re.sub(r"[\(\[].*?[\)\]]", "", entry.name) if entry.name else ""

            logger.debug("%s: Import even found: %s", feed, title)

            # Check if we already have the event stored
            original = Event.objects.filter(start_time=start_date, title=title).first()

            # If we get the event from API it should not be removed
            if original:
                logger.debug("%s: Event: %s already in database, skipping", feed, title)

                # Remove the found fleet from the to be removed list
                event_ids_to_remove.discard(original.id)

            else:
                # Save new event to database
                event = Event(
                    operation_type=feed.operation_type,
                    title=title,
                    host=feed.host,
                    formup_system=entry.location,
                    description=strip_tags(entry.description.replace("<br>", "\n")),
                    start_time=start_date,
                    end_time=end_date,
                    external=True,
                    user=feed.creator,
                    event_visibility=feed.event_visibility,
                    eve_character=feed.eve_character,
                )

                logger.debug(
                    "%s: Saved new EVE UNI event in database: %s",
                    feed,
                    title,
                )
                event.save()

    except (NotImplementedError, RequestException):
        logger.error("%s: Error in fetching fleets", feed, exc_info=True)
        return True

    return False


@shared_task(
    **{
        **TASK_ESI_KWARGS,
        **{
            "base": QueueOnce,
            "once": {"keys": ["owner_pk"], "graceful": True},
            "max_retries": None,
        },
    }
)
def update_events_for_owner(self, owner_pk):
    """fetches all calendars for owner from ESI"""

    return _get_owner(owner_pk).update_events_esi()


@shared_task(**TASK_DEFAULT_KWARGS)
def update_all_ingame_events():
    for owner in Owner.objects.all():
        update_events_for_owner.apply_async(
            kwargs={"owner_pk": owner.pk},
            priority=DEFAULT_TASK_PRIORITY,
        )


def _get_owner(owner_pk: int) -> Owner:
    """returns the owner or raises exception"""
    try:
        owner = Owner.objects.get(pk=owner_pk)
    except Owner.DoesNotExist:
        raise Owner.DoesNotExist(
            "Requested owner with pk {} does not exist".format(owner_pk)
        )
    return owner


# @shared_task
# def add(x, y):
#     return x + y
