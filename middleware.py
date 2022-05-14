from typing import TYPE_CHECKING
import uuid
import logging

from .models import WebEvent
if TYPE_CHECKING:
    from django.http import HttpResponse


logger = logging.getLogger(__name__)


class AnalyticsMiddleware:

    scout_id:str = ""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # don't track django admin
        if request.path.startswith("/admin") or request.path.startswith("/404"):
            return self.complete(request)

        meta_attrs = [
            "HOSTNAME",
            "PYTHON_VERSION",
            "PYTHON_SETUPTOOLS_VERSION",
            "STATIC_DEBUG",
            "LANG",
            "PYTHONPATH",
            "TERM",
            "SHLVL",
            "PYTHON_PIP_VERSION",
            "PYTHON_GET_PIP_SHA256",
            "TZ",
            "SERVER_NAME",
            "GATEWAY_INTERFACE",
            "SERVER_PORT",
            "REMOTE_HOST",
            "CONTENT_LENGTH",
            "SCRIPT_NAME",
            "SERVER_PROTOCOL",
            "SERVER_SOFTWARE",
            "REQUEST_METHOD",
            "PATH_INFO",
            "QUERY_STRING",
            "REMOTE_ADDR",
            "CONTENT_TYPE",
            "HTTP_HOST",
            "HTTP_CONNECTION",
            "HTTP_CACHE_CONTROL",
            "HTTP_SEC_CH_UA",
            "HTTP_SEC_CH_UA_MOBILE",
            "HTTP_SEC_CH_UA_PLATFORM",
            "HTTP_UPGRADE_INSECURE_REQUESTS",
            "HTTP_USER_AGENT",
            "HTTP_ACCEPT",
            "HTTP_SEC_FETCH_SITE",
            "HTTP_SEC_FETCH_MODE",
            "HTTP_SEC_FETCH_USER",
            "HTTP_SEC_FETCH_DEST",
            "HTTP_REFERER",
            "HTTP_ACCEPT_ENCODING",
            "wsgi.run_once",
            "wsgi.url_scheme",
            "wsgi.multithread",
            "wsgi.multiprocess",
        ]
        full_event = {
            prop.lower().replace(".", "_"): request.META.get(prop)
            for prop in meta_attrs
        }
        self.scout_id = self._get_scout_id(request)
        event = dict(
            user_id=request.user.id,
            absolute_uri=request.build_absolute_uri(),
            scout_id = self.scout_id,
            **self._cookies(request.COOKIES),
            full_event=full_event
        )

        try:
            WebEvent.objects.create(**event)
        except Exception as e:
            logger.error("unable to save analytics to db: %s", e)

        return self.complete(request)

    def complete(self, request):

        response = self.get_response(request)
        response.set_cookie("scout",
                            self.scout_id,
                            max_age=(60*60*24*365*10))
        return response

    @classmethod
    def _get_scout_id(cls, request) -> "HttpResponse":
        """create a scout tag for the pre-session request"""
        return request.COOKIES.get("scout",
                                   str(uuid.uuid4()))

    @classmethod
    def _cookies(cls, cookies: dict) -> dict:
        return dict(
            session_id=cookies.get("sessionid"),
            # extra context if using GA tracker
            google_analytics_client_id=cookies.get("_ga",None),
        )
