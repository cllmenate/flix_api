from django.db import models


NATIONALITIES = [
    ('AUSTRALIA', 'Austrália'),
    ('BRAZIL', 'Brasil'),
    ('CANADA', 'Canadá'),
    ('CHINA', 'China'),
    ('FRANCE', 'França'),
    ('GERMANY', 'Alemanha'),
    ('INDIA', 'Índia'),
    ('ITALY', 'Itália'),
    ('UK', 'Reino Unido'),
    ('USA', 'Estados Unidos'),
    ('OTHER', 'Outro'),
]


# Create your models here.
class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(
        max_length=50,
        choices=NATIONALITIES,
        blank=True,
        null=True
    )
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"
        ordering = ['name']
