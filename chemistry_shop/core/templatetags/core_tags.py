from django import template
from core.models import *

register = template.Library()


@register.inclusion_tag('core/categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, "cat_selected": cat_selected}


@register.inclusion_tag('core/menu.html')
def show_menu():
    menu = [
        {'title': 'Home', 'url_name': 'home'},
        {'title': 'About', 'url_name': 'about'},
        {'title': 'Contact', 'url_name': 'contact'},
        {'title': 'Products', 'url_name': 'home'},
    ]
    return {"menu": menu}


@register.inclusion_tag('core/footer.html')
def show_footer():
    footer = [
        {'title': 'Home', 'url_name': 'home'},
        {'title': 'About', 'url_name': 'about'},
        {'title': 'Contact', 'url_name': 'contact'}
    ]
    return {"footer": footer}
