from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from movies.models import Movie


# Create your models here.
class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(0, 'Rating must be at least 0'),
            MaxValueValidator(5, 'Rating must be at most 5')
        ]
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Review for {self.movie.title} - Rating: {self.rating}'
