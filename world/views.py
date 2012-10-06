from world.models import World, Cell

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib.gis.geos import Point, Polygon


def index(request):
    """
    Loads the world index.
    """
    env = {}
    template = 'index.html'

    worlds = World.objects.all()
    env['world'] = worlds

    return TemplateResponse(request, template, env)


def detail(request, slug, x=0, y=0):
    """
    Returns the detail view of a world.
    """
    env = {}
    template = 'detail.html'

    # Ensure that the x and y variables are integers
    x = int(x)
    y = int(y)

    world = get_object_or_404(World, slug=slug)
    board = Polygon([
        (x, y),
        (x, y + 4),
        (x + 4, y + 4),
        (x + 4, y),
        (x, y),
        ])
    cells = world.cells.filter(location__contained=board)

    env['world'] = world
    env['cells'] = cells
    env['scale'] = 'large'

    return TemplateResponse(request, template, env)


def cell_by_id(request, cell_id):
    cell = get_object_or_404(Cell, id=cell_id)
    return cell_view(request, cell)


def cell_by_location(request, slug, x, y):
    world = get_object_or_404(World, slug=slug)

    point = Point(x, y)
    try:
        cell = world.cells.get(location=point)
    except Cell.DoesNotExist:
        cell = Cell(location=point, is_alive=False)
    return cell_view(request, cell)

import json


def cell_view(request, cell):
    env = {}
    if cell.id is not None:
        env['id'] = cell.id
    env['x'] = cell.location.x
    env['y'] = cell.location.y
    env['is_alive'] = cell.is_alive
    env['generation'] = cell.generation_id
    env['world'] = cell.generation.world_id
    return HttpResponse(json.dumps(env), mimetype='application/json')
