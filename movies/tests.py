import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from actors.models import Actor
from genres.models import Genre
from movies.models import Movie


class MovieAPITests(APITestCase):
    """
    Tests for the Movie API, ensuring all fields, including 'duration', are handled correctly.
    """

    def setUp(self):
        """Set up data for the tests."""
        # Create a user for authentication
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        # Grant permissions for movie views
        content_type = ContentType.objects.get_for_model(Movie)
        post_permission = Permission.objects.get(
            codename='add_movie',
            content_type=content_type,
        )
        get_permission = Permission.objects.get(
            codename='view_movie',
            content_type=content_type,
        )
        self.user.user_permissions.add(post_permission, get_permission)

        # Create related objects (assuming simple models for Genre and Actor)
        self.genre = Genre.objects.create(name='Sci-Fi')
        self.actor1 = Actor.objects.create(name='Leonardo DiCaprio', date_of_birth=datetime.date(1974, 11, 11), nationality='USA')
        self.actor2 = Actor.objects.create(name='Keanu Reeves', date_of_birth=datetime.date(1964, 9, 2), nationality='CANADA')

        # Create movie instances
        self.movie1 = Movie.objects.create(
            title="Inception",
            genre=self.genre,
            release_date=datetime.date(2010, 7, 16),
            duration=148,
            description="A thief who steals corporate secrets through the use of dream-sharing technology."
        )
        self.movie1.actors.add(self.actor1)

        self.movie2 = Movie.objects.create(
            title="The Matrix",
            genre=self.genre,
            release_date=datetime.date(1999, 3, 31),
            duration=136,
            description="A computer hacker learns from mysterious rebels about the true nature of his reality."
        )
        self.movie2.actors.add(self.actor2)

    def test_get_movie_list(self):
        """
        Ensure we can retrieve a list of movies and that 'duration' is present.
        """
        url = reverse("movie-create-list-view")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Find the 'Inception' movie dict in the response list (order isn't guaranteed)
        inception_data = next((movie for movie in response.data if movie['title'] == 'Inception'), None)
        self.assertIsNotNone(inception_data)

        # The response data uses MovieListDetailSerializer
        self.assertEqual(inception_data['title'], 'Inception')
        self.assertEqual(inception_data['duration'], 148)
        self.assertIn('duration', inception_data)
        self.assertIn('rate', inception_data)  # Also check for the SerializerMethodField

    def test_get_movie_detail(self):
        """
        Ensure we can retrieve a single movie's details, including 'duration'.
        """
        url = reverse("movie-detail-view", kwargs={"pk": self.movie1.pk})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # The response.data here is the dictionary for the movie from MovieListDetailSerializer
        # Note: This assumes the structure of your ActorSerializer and GenreSerializer
        expected_movie_dict = {
            'id': self.movie1.id,
            'title': 'Inception',
            'genre': {
                'id': self.genre.id,
                'name': 'Sci-Fi',
                'description': None  # Assuming GenreSerializer includes this field
            },
            'description': 'A thief who steals corporate secrets through the use of dream-sharing technology.',
            'release_date': '2010-07-16',
            'duration': 148,
            'rate': None,  # Assuming no reviews yet
            'actors': [{
                'id': self.actor1.id,
                'name': 'Leonardo DiCaprio',
                'date_of_birth': '1974-11-11',
                'nationality': 'USA',
                'biography': None
            }]
        }
        self.assertEqual(response.data, expected_movie_dict)
        self.assertIn('duration', response.data)

    def test_create_movie(self):
        """
        Ensure we can create a new movie and that 'duration' is handled correctly.
        """
        url = reverse("movie-create-list-view")
        new_genre = Genre.objects.create(name='Thriller')
        data = {
            "title": "Parasite",
            "genre": new_genre.id,
            "release_date": "2019-05-30",
            "duration": 132,
            "description": "A poor family, the Kims, con their way into becoming the servants of a rich family, the Parks."
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 3)

        # The response for a POST uses MovieSerializer, which returns all fields
        self.assertEqual(response.data['title'], "Parasite")
        self.assertEqual(response.data['duration'], 132)
        self.assertIn('duration', response.data)

    def test_create_movie_invalid_duration(self):
        """
        Ensure creating a movie with an invalid duration (e.g., negative) fails.
        """
        url = reverse("movie-create-list-view")
        data = {
            "title": "Invalid Movie",
            "genre": self.genre.id,
            "release_date": "2023-01-01",
            "duration": -100,  # PositiveIntegerField should reject this
            "description": "A movie with negative duration."
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('duration', response.data)
        # Check for the Portuguese validation message from PositiveIntegerField
        self.assertIn('maior ou igual a 0', str(response.data['duration'][0]))

    def test_unauthenticated_access_fails(self):
        """
        Ensure unauthenticated users cannot access the movie list.
        """
        # Log out the user
        self.client.force_authenticate(user=None)

        url = reverse("movie-create-list-view")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
