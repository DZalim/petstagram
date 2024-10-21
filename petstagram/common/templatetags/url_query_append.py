from django import template

register = template.Library()


@register.simple_tag()
def url_query_append_tag(request, field, value):  # field = page or pet_name
    # field = "page"; value= 2
    dict_ = request.GET.copy()  # request.GET => {"pet_name": "barni"}
    dict_[field] = value  # {"pet_name": "barni", "page": 2}

    return dict_.urlencode()  # {"pet_name": "barni", "page": 2} => ?pet_name=barni&page=2
