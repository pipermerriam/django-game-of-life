from world.models import World

#from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse


def index(request):
    """
    Loads the world index.
    """
    env = {}
    template = 'index.html'

    worlds = World.objects.all()
    env['world'] = worlds

    return TemplateResponse(request, template, env)


def detail(request):
    """
    Returns the detail view of a world.
    """
    env = {}
    template = 'detail.html'

    return TemplateResponse(request, template, env)
