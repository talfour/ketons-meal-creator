from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import json


register = template.Library()

from ..models import Recipe

@register.simple_tag
def total_recipes():
    return Recipe.objects.filter(published=True).count()

@register.simple_tag
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price
    
@register.simple_tag
def get_most_liked_recipe(count=6):
    recipes_by_popularity = Recipe.objects.filter(published=True).order_by('-total_likes')
    return recipes_by_popularity[:count]

@register.inclusion_tag('recipes/latest_recipes.html')
def show_latest_recipes(count=6):
    latest_recipes = Recipe.objects.filter(published=True).order_by('-created')[:count]
    return {'latest_recipes': latest_recipes}

def parse_paragraph(text):
    return f'<p>{text}</p>'


def parse_list(items):
    list_li = ''.join([f'<li>{item}</li>' for item in items])
    return f'<ul>{list_li}</ul>'


def parse_header(text, level):
    return f'<h{level}>{text}</h{level}>'

def parse_image(image, caption):
    return f"<figure><img src='{image}'></image><figcaption>{caption}</figacption></figure>"


@register.filter(is_safe=True)
def editorjs(value):
    try:
        value = json.loads(value)
        if not isinstance(value, dict):
            return value
    

        html_list = []
        for item in value['blocks']:
            
            if item['type'] == 'paragraph':
                html_list.append(parse_paragraph(
                    item['data']['text'].replace('&nbsp;', ' ')))
            elif item['type'] == 'Header':
                html_list.append(parse_header(
                    item['data']['text'].replace('&nbsp;', ' '), item['data']['level']))
            elif item['type'] == 'List':
                html_list.append(parse_list(item['data']['items']))

            elif item['type'] == "Image":

                html_list.append(parse_image(item['data']['file']['url'], item['data']['caption']))

        return mark_safe(''.join(html_list))
    except:
        print('error')