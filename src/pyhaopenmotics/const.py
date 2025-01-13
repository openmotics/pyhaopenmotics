"""Asynchronous Python client for the OpenMotics API."""

from __future__ import annotations

CLOUD_BASE_URL = "https://api.openmotics.com/api"
CLOUD_API_VERSION = "v1.1"

#   "configure.outputs configure view.sensors control view.thermostats " \
#   "control.ventilation view.energy configure.thermostats view.outputs " \
#   "view.event_rules control.thermostats view.energy.reports control.outputs" \
#   "view.installations"
CLOUD_SCOPE = "control view configure"

CLOUD_API_URL = f"{CLOUD_BASE_URL}/{CLOUD_API_VERSION}"
OAUTH2_TOKEN = f"{CLOUD_API_URL}/authentication/oauth2/token"  # nosec
OAUTH2_AUTHORIZE = f"{CLOUD_API_URL}/authentication/oauth2/authorize"
