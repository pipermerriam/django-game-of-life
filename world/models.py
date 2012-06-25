from django.contrib.gis.db import models
from django.contrib.gis.db.models import Max

from django_extensions.db.fields import AutoSlugField

from gameoflife.behaviors import Queryable

from fusionbox.behaviors import Timestampable


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

    def __unicode__(self):
        return self.title

    @property
    def cells(self):
        return self.generations.order_by('-generation')[0].cells.all()


class Generation(Timestampable, Queryable):
    """
    A `Generation` is an organizational unit with a world to record the history
    of cells.  Once a generation has been fully generated, a hash of it's cells
    is created.

    The generation hash is the bitwise xor of all of the cell coordinates and
    states ordered by latitude, then longitude.
    """
    generation = models.PositiveIntegerField(blank=True)
    world = models.ForeignKey(World, related_name='generations')

    hash = models.CharField(max_length=255)

    class Meta:
        unique_together = ('world', 'generation')

    def save(self, *args, **kwargs):
        if self.generation is None:
            if not self.world.generations.exists():
                self.generation = 0
            else:
                self.generation = self.world.generations.aggregate(Max('generation'))['generation__max'] + 1
        super(Generation, self).save(*args, **kwargs)

    def __unicode__(self):
        if not self.id:
            return u'{world} - unsaved generation'.format(
                    world=unicode(self.world),
                    )
        return u'{world} - generation {i}'.format(
                world=unicode(self.world),
                i=self.generation,
                )


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
    child = models.OneToOneField('self', related_name='parent', blank=True, null=True)

    is_alive = models.NullBooleanField()

    location = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{world} - point - generation {i}'.format(
                world=unicode(self.generation.world),
                i=self.generation.generation,
                )
