from django.db import models
from actors.models import Actor
from genres.models import Genre


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.ForeignKey(
        Genre, 
        on_delete=models.PROTECT, 
        related_name='movies'
    )
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    actors = models.ManyToManyField(
        Actor, 
        related_name='movies', 
        blank=True
    )

    def __str__(self):
        return self.title