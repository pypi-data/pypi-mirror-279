"""
This module contains helpers for the TextLab API client
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.http import HttpRequest

    from integreat_cms.cms.models.events.event_translation import EventTranslation
    from integreat_cms.cms.models.pages.page_translation import PageTranslation
    from integreat_cms.cms.models.pois.poi_translation import POITranslation

logger = logging.getLogger(__name__)


def check_hix_score(
    request: HttpRequest,
    source_translation: EventTranslation | (PageTranslation | POITranslation),
    show_message: bool = True,
) -> bool:
    """
    Check whether the required HIX score is met and it is not ignored

    :param request: The current request
    :param source_translation: The source translation
    :param show_message: whether the massage should be shown to users.
    :return: Whether the HIX constraints are valid
    """
    if not source_translation.hix_enabled:
        return True
    if not source_translation.hix_sufficient_for_mt:
        if show_message:
            messages.error(
                request,
                _(
                    'HIX score {:.2f} of "{}" is too low for machine translation (minimum required: {})'
                ).format(
                    source_translation.hix_score,
                    source_translation,
                    settings.HIX_REQUIRED_FOR_MT,
                ),
            )
        return False
    if source_translation.hix_ignore:
        if show_message:
            messages.error(
                request,
                _(
                    'Machine translations are disabled for "{}", because its HIX value is ignored'
                ).format(
                    source_translation.title,
                ),
            )
        return False
    logger.debug(
        "HIX score %.2f of %r is sufficient for machine translation",
        source_translation.hix_score,
        source_translation,
    )
    return True
