from django.db import models

# Create your models here.

class DPrevUser(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200)

class Game(models.Model):
    creator = models.ForeignKey(DPrevUser, on_delete=models.CASCADE)

class GameResult(models.Model):
    player = models.ForeignKey(DPrevUser, on_delete=models.CASCADE)
    game_played = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()
    datetime_reached = models.DateTimeField(auto_now_add=True)

class PhotoNamePair(models.Model):
    game_with_photo = models.ForeignKey(Game, on_delete=models.CASCADE)
    photo_link = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
