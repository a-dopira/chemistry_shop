from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.cache import cache


def serve_cached_image(request, model_name, cache_key):

    image_data = cache.get(cache_key)

    if not image_data:
        raise Http404("Image not found")

    return HttpResponse(
        image_data,
        content_type="image/jpeg",
        headers={
            "Cache-Control": "public, max-age=2592000",
            "Expires": "Thu, 31 Dec 2025 23:59:59 GMT",
        },
    )


def about(request):
    context = {
        "title": "Information page | The Hag's cure",
        "text": "We supply 1,000+ ingredients of the highest quality packaged in convenient retail sizes but also "
        "large bulk sizes at discount rates. We are ISO certified, FDA registered, and USDA organic certified.",
    }
    return render(request, "core/about.html", context=context)


def contacts(request):
    context = {
        "title": "Contacts",
        "social_media": [
            ("instagram", "https://www.instagram.com/dizainmebli/"),
            ("facebook", "https://www.facebook.com/a.dopira.u/"),
            ("github", "https://github.com/a-dopira"),
            ("linkedIn", "https://www.linkedin.com/in/anton-dopira-15b8b9210/"),
        ],
    }
    return render(request, "core/contacts.html", context=context)
