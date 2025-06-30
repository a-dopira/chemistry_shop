from django.db.models import Q
from django.http import HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView

from .models import Category, Ingredient


class SingleProduct(DetailView):
    model = Ingredient
    template_name = "store/single_product.html"
    context_object_name = "prod"
    slug_url_kwarg = "prod_slug"

    def get_quantity_range(self, prod):
        return range(1, prod.quantity + 1) if prod.is_in_stock else []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prod = context["prod"]

        context.update(
            {
                "title": f"{prod.title} | {prod.cat.name}",
                "cat_selected": prod.cat.id,
                "quantity_range": self.get_quantity_range(prod),
            }
        )
        return context


class IngredientsList(ListView):
    paginate_by = 3
    model = Ingredient
    template_name = "store/showcase.html"
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
            category = context["products"][0].cat
            context.update({
                "category": category,
                "cat_selected": category.pk,
                "title": f"{category.name} | Categories",
                "is_category": True,
            })

        if self.request.htmx:
            current_page = int(self.request.GET.get("page", 1))
            context["total_shown"] = current_page * self.paginate_by
            context["total_items"] = self.get_queryset().count()
            context["target_container"] = "products-container"

        return context

    def get_template_names(self):
        if self.request.htmx:
            load_more = self.request.GET.get("load_more")
            if load_more:
                return ["store/partials/load_more_response.html"]
            else:
                return ["store/partials/products_page.html"]
        return [self.template_name]


class FormSearch(ListView):
    model = Ingredient
    template_name = "store/showcase.html"
    context_object_name = "products"
    paginate_by = 3

    def get_paginate_by(self, queryset):
        if self.request.htmx and "search-results" in str(
            self.request.headers.get("HX-Target", "")
        ):
            return 2
        return 3

    def get_queryset(self):
        query = self.request.GET.get("search", "")

        if not query and hasattr(self.request, "session"):
            query = self.request.session.get("last_search_query", "")

        if query:
            products = Ingredient.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            return products

        return Ingredient.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("search", "")

        if not query and hasattr(self.request, "session"):
            query = self.request.session.get("last_search_query", "")

        if query and hasattr(self.request, "session"):
            self.request.session["last_search_query"] = query

        context.update(
            {
                "cat_selected": 0,
                "query": query,
                "title": f"Search results for '{query}'" if query else "Search Results",
                "is_search": True,
            }
        )

        return context

    def get_template_names(self):
        if self.request.htmx and "search-results" in str(
            self.request.headers.get("HX-Target", "")
        ):
            return ["store/search_dropdown.html"]

        if self.request.htmx:
            load_more = self.request.GET.get("load_more")
            if load_more:
                return ["store/partials/load_more_response.html"]
            else:
                return ["store/partials/products_page.html"]

        return [self.template_name]


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
