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


def detail(request, slug):
    """
    Returns the detail view of a world.
    """
    env = {}
    template = 'detail.html'

    cells = []
    import random
    from world.models import Cell
    for y in range(20):
        row = []
        for x in range(20):
            row.append(Cell(is_alive=bool(random.getrandbits(1)), long=x, lat=y))
        cells.append(row)

    env['cells'] = cells
    env['scale'] = 'large'

    return TemplateResponse(request, template, env)
