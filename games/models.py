from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 
from django.contrib.auth import get_user_model


class GameReview(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    gameId = models.IntegerField()
    review = models.TextField(blank=True)
    rating = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(10)], max_digits=4, decimal_places=1)
    favourite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title