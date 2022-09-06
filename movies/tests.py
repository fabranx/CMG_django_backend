from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from .models import MovieReview

class MovieReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(
            username='ciccio',
            email='ciccio@email.com',
            password='testpass123',
        )
        MovieReview.objects.create(
            author = user,
            title = 'The Last Duel',
            movieId = '24601',
            review = 'Film stupendo',
            rating = '9',
            favourite = True
        )

    def test_moviereview_content(self):
        movie = MovieReview.objects.get(id=1)
        expected_object_name = f'{movie.title}'
        self.assertEqual(expected_object_name, 'The Last Duel')
        expected_author = f'{movie.author}'
        self.assertEqual(expected_author, 'ciccio')
        expected_movieId = f'{movie.movieId}'
        self.assertEqual(expected_movieId, '24601')
        expected_review = f'{movie.review}'
        self.assertEqual(expected_review, 'Film stupendo')
        expected_rating = f'{movie.rating}'
        self.assertEqual(expected_rating, '9.0')
        expected_favourite = f'{movie.favourite}'
        self.assertTrue(expected_favourite)


