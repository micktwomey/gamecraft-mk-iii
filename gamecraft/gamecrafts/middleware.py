"""Middleware for GameCraft"""

import logging


class HttpRequestLoggingMiddleware(object):
    """Logs HTTP request information"""
    def process_request(self, request):
        log = logging.getLogger("request")
        try:
            log.info(
                " ".join(
                    (
                        str(x) for x in
                        (
                            request.method,
                            request.path,
                            request.META.get("CONTENT_LENGTH"),
                            repr(request.META.get("CONTENT_TYPE")),
                            request.META.get("HTTP_HOST"),
                            request.META.get("REMOTE_ADDR"),
                            request.META.get("REMOTE_HOST"),
                            repr(request.META.get("HTTP_REFERER")),
                            repr(request.META.get("HTTP_USER_AGENT")),
                        )
                    )
                )
            )
        except Exception:
            log.exception("Ooops")
