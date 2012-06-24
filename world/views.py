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


def detail(request, slug, lat=0, long=0):
    """
    Returns the detail view of a world.
    """
    env = {}
    template = 'detail.html'

    lat = int(lat)
    long = int(long)

    cells = []
    from world.models import Cell
    for y in range(long + 4, long - 1, -1):
        row = []
        for x in range(lat, lat + 5):
            row.append(Cell.objects.get(lat=x, long=y))
        cells.append(row)

    env['cells'] = cells
    env['scale'] = 'large'

    return TemplateResponse(request, template, env)


def cells(request, cell_id):
    pass
