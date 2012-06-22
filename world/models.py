from django.contrib.gis.db import models

from django_extensions.db.fields import AutoSlugField

from gameoflife.behaviors import Timestampable, Queryable


class World(Timestampable, Queryable):
    """
    A `World` is the parent class that organizes one game from another.  A
    `World` consists of a collection of `Cell` instances which make up the game
    board.

    A `World` has no boundaries and can grow infinitely in every direction.

    Each turn every cell whic is either alive, or adjacent to a cell which is
    alive continues onto the next state of the world.  A `World` can exist in
    one of three states, (active, paused, or stable).

        - `active`: Actively evolving new `Generation`s
        - `paused`: Evolution paused.
        - `stable`: World has reached a stable state.

    A world is considered stable if there is a repeating pattern of at least 8
    successive `Generation`s.
    """
    STATE_CHOICES = (
            ('active', 'Active'),
            ('paused', 'Paused'),
            ('stable', 'Stable'),
            )
    state = models.CharField(max_length=255, choices=STATE_CHOICES, blank=True, default='paused')
    title = models.CharField(max_length=255)

    slug = AutoSlugField(populate_from='title')


class Generation(Timestampable, Queryable):
    """
    A `Generation` is an organizational unit with a world to record the history
    of cells.  Once a generation has been fully generated, a hash of it's cells
    is created.

    The generation hash is the bitwise xor of all of the cell coordinates and
    states ordered by latitude, then longitude.
    """
    generation = models.PositiveIntegerField()
    world = models.ForeignKey(World, related_name='generations')

    hash = models.CharField(max_length=255)


class Cell(Timestampable):
    """
    Each `Cell` represents a square on the game board.

    Death:
    - Less than 2 neighbors.
    - Greater than 3 neighbors.

    Birth
    - Dead cell with exactly 3 living neighbors.
    """
    generation = models.ForeignKey(Generation, related_name='cells')
    child = models.OneToOneField('self', related_name='parent')

    is_alive = models.NullBooleanField()

    lat = models.IntegerField()
    long = models.IntegerField()
