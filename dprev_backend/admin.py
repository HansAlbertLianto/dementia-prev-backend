from django.contrib import admin
from dprev_backend.models import DPrevUser, Game, GameResult, PhotoNamePair, ShuffledGame, PhotoNameQuestion

# Register your models here.

admin.site.register(DPrevUser)
admin.site.register(Game)
admin.site.register(GameResult)
admin.site.register(PhotoNamePair)
admin.site.register(ShuffledGame)
admin.site.register(PhotoNameQuestion)
