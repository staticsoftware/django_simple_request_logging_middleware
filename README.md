# Django Simple Request Logging Middleware
This does exactly what it says it does - log requests.
It adds a few colorful helpers:
- `scout_id` is a uuid cookie assigned on the very first "handshake" request, making it easy to attribute visits before the client-side has a chance to fire.
- `google_analytics_client_id` for leveraging and stitching to GA.

There is a reasonable performance concern with assigning a uuid to requests, however this hit is only for the first request with cookied sessions. We haven't optimized for non-cookied requests, and the performance hit is negligable otherwise; if this is a problem for your use case, this super simple implementation is probably not the right fit.

## Using
1. install by cloning this repo (we will add to pypi soon promise!)

```
git clone && python3 -m pip install .
```
2. add to your `INSALLLED_APPS` and `MIDDLEWARE`:

```
INSTALLED_APS = [
    ...
    "django_simple_request_logging_middleware",
    ...
]
...

# add to the end of your middleware
MIDDLEWARE = [
    ...
    "django_simple_request_logging_middleware.middleware.AnalyticsMiddleware"
]
```

You can now view events in the django admin.

## Cleaning Up
Left unchecked these events can clog up your production database. To prevent that you likely want to extract them to a Data Warehouse and then purge them from your prod db. This package ships with the `analytics_cleanup` manage.py command that will purge all existing events; you can schedule this command via cron job or something more complex like [django_q](https://django-q.readthedocs.io/en/latest/).