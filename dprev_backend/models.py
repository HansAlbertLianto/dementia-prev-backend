from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class DPrevUserManager(models.Manager):
    def create_dprevuser(self, user, full_name, email):
        dprevuser = self.create(user=user, full_name=full_name, email=email)
        return dprevuser

# Users of DementiaPrev
class DPrevUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    REQUIRED_FIELDS = ['full_name', 'email']

    objects = DPrevUserManager()

# A game created by a user of DementiaPrev
class Game(models.Model):
    creator = models.ForeignKey(DPrevUser, related_name='games_made', on_delete=models.CASCADE)
    gamename = models.CharField(max_length=100, unique=True)

# A shuffled game
class ShuffledGame(models.Model):
    base_game = models.ForeignKey(Game, related_name='game_instances', on_delete=models.CASCADE)

# The end-result of one particular game
class GameResult(models.Model):
    player = models.ForeignKey(DPrevUser, related_name='user_result_history', on_delete=models.CASCADE)
    game_instance_played = models.OneToOneField(ShuffledGame, related_name='game_result', on_delete=models.CASCADE)
    game_played = models.ForeignKey(Game, related_name='game_result_history', on_delete=models.CASCADE)
    score = models.IntegerField()
    datetime_reached = models.DateTimeField(auto_now_add=True)

# Correct question and answer in the game
class PhotoNamePair(models.Model):
    game_with_photo = models.ForeignKey(Game, related_name='photo_name_pairs', on_delete=models.CASCADE)
    photo_link = models.ImageField(upload_to='photos')
    name = models.CharField(max_length=100)

# One question and answer in the game
class PhotoNameQuestion(models.Model):
    game_with_photo = models.ForeignKey(ShuffledGame, related_name='questions', on_delete=models.CASCADE)
    corresponding_photo = models.ForeignKey(PhotoNamePair, related_name='photo_questions', on_delete=models.CASCADE, blank=True, null=True)
    default_photo_link = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    correct = models.BooleanField(default=True)

