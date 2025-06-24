import os
import redis
from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)


# periodic tasks


@shared_task
def cleanup_expired_sessions():
    """cleanup expired sessions that are older than 3 days"""
    try:
        expired_count = Session.objects.filter(expire_date__lt=timezone.now()).count()
        Session.objects.filter(expire_date__lt=timezone.now()).delete()

        return f"Deleted {expired_count} expired sessions"

    except Exception as e:
        return f"Error: {e}"


@shared_task
def cleanup_blacklisted_tokens():
    """cleanup blacklisted tokens that are older than 7 days"""
    try:

        week_ago = timezone.now() - timedelta(days=7)

        blacklisted_count = BlacklistedToken.objects.filter(
            token__created_at__lt=week_ago
        ).count()

        BlacklistedToken.objects.filter(token__created_at__lt=week_ago).delete()

        outstanding_count = OutstandingToken.objects.filter(
            created_at__lt=week_ago, blacklistedtoken__isnull=False
        ).count()

        OutstandingToken.objects.filter(
            created_at__lt=week_ago, blacklistedtoken__isnull=False
        ).delete()

        total_blacklisted = BlacklistedToken.objects.count()
        total_outstanding = OutstandingToken.objects.count()

        result = {
            "removed_blacklisted": blacklisted_count,
            "removed_outstanding": outstanding_count,
            "remaining_blacklisted": total_blacklisted,
            "remaining_outstanding": total_outstanding,
        }

        return f"Removed {blacklisted_count} blacklisted and {outstanding_count} outstanding tokens"

    except Exception as e:
        return f"Error: {e}"


@shared_task
def system_health_check():
    try:
        r = redis.Redis(host="localhost", port=6379, db=1)
        r.ping()

        test_key = "health_check_test"
        cache.set(test_key, "ok", timeout=60)
        if cache.get(test_key) != "ok":
            raise Exception("Cache write/read failed")
        cache.delete(test_key)

        if not os.path.exists(settings.MEDIA_ROOT):
            raise Exception("MEDIA_ROOT not accessible")

        return "System health: OK"

    except Exception as e:
        return f"Health check failed: {e}"
