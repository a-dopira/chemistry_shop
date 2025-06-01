from django.shortcuts import render
from django.views.generic import ListView
from django.http import Http404

from store.models import Ingredient, Category


class IngredientsList(ListView):
    paginate_by = 3
    model = Ingredient
    template_name = "core/home.html"
    context_object_name = "products"

    def get_queryset(self):
        cat_slug = self.kwargs.get("cat_slug")
        if cat_slug:
            return Ingredient.objects.filter(cat__slug=cat_slug).select_related("cat")
        return Ingredient.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        cat_slug = self.kwargs.get("cat_slug")
        if cat_slug:
            try:
                category = Category.objects.get(slug=cat_slug)
                context.update(
                    {
                        "category": category,
                        "cat_selected": category.pk,
                        "title": f"{category.name} | Categories",
                        "is_category": True,
                    }
                )
            except Category.DoesNotExist:
                raise Http404("Category does not exist")
        else:
            context.update(
                {
                    "cat_selected": 0,
                    "title": "The Hag's Cure",
                }
            )

        if self.request.htmx:
            current_page = int(self.request.GET.get("page", 1))
            context["total_shown"] = current_page * self.paginate_by
            context["total_items"] = self.get_queryset().count()

        return context

    def get_template_names(self):
        if self.request.htmx:
            load_more = self.request.GET.get("load_more")
            if load_more:
                return ["store/partials/load_more_response.html"]
            else:
                return ["store/partials/products_page.html"]
        return [self.template_name]


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
