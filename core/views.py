from django.shortcuts import render


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
