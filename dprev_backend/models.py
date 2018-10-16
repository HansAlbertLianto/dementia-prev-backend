from django.db import models

# Create your models here.

# Users of DementiaPrev
class DPrevUser(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200)

# A game created by a user of DementiaPrev
class Game(models.Model):
    creator = models.ForeignKey(DPrevUser, related_name='games_made', on_delete=models.CASCADE)

# The end-result of one particular game
class GameResult(models.Model):
    player = models.ForeignKey(DPrevUser, related_name='user_result_history', on_delete=models.CASCADE)
    game_played = models.ForeignKey(Game, related_name='game_result_history', on_delete=models.CASCADE)
    score = models.IntegerField()
    datetime_reached = models.DateTimeField(auto_now_add=True)

# One question in the game
class PhotoNamePair(models.Model):
    game_with_photo = models.ForeignKey(Game, related_name='photo_name_pairs', on_delete=models.CASCADE)
    photo_link = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
