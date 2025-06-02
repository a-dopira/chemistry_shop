from django import template
from store.models import Category

register = template.Library()


@register.inclusion_tag("core/categories.html")
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag("core/partials/hybrid_pagination.html")
def show_hybrid_pagination(page_obj, target_id, mode="pagination"):
    """
    Гибридная пагинация с переключением режимов

    Args:
        page_obj: объект страницы Django
        target_id: ID элемента для замены контента
        mode: 'pagination' или 'load_more'
    """
    return {
        "page_obj": page_obj,
        "paginator": page_obj.paginator,
        "target_id": target_id,
    }


@register.inclusion_tag("core/menu.html")
def show_menu():
    menu = [
        {"title": "About", "url_name": "about"},
        {"title": "Contact", "url_name": "contact"},
    ]
    return {"menu": menu}


@register.inclusion_tag("core/footer.html")
def show_footer():
    footer = [
        {"title": "Home", "url_name": "showcase"},
        {"title": "About", "url_name": "about"},
        {"title": "Contact", "url_name": "contact"},
    ]
    return {"footer": footer}
