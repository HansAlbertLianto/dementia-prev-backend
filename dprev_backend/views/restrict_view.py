from dprev_backend.models import Game, DPrevUser, ShuffledGame
from dprev_backend.serializers import GameSerializer, DPrevUserSerializer, ShuffledGameSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

# Restrict to one game
@csrf_exempt
def game_details(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except game.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GameSerializer(game)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = GameSerializer(game, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        game.delete()
        return HttpResponse(status=204)

# Restrict to one user
@csrf_exempt
def user_details(request, username):
    try:
        user = DPrevUser.objects.get(user__username=username)
    except user.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DPrevUserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DPrevUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)

# Get one game instance
@csrf_exempt
def shuffledgame_details(request, gamename):

    game = Game.objects.get(gamename=gamename)
    shuffled_game = game.game_instances.get(pk=ShuffledGame.objects.count())

    serializer = ShuffledGameSerializer(shuffled_game)

    return JsonResponse(serializer.data)