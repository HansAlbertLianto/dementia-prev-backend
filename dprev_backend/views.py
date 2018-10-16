from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from dprev_backend.models import GameResult, PhotoNamePair, Game, DPrevUser
from dprev_backend.serializers import UserSerializer, GroupSerializer, GameResultSerializer, PhotoNamePairSerializer, GameSerializer, DPrevUserSerializer
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class Authentication:

    # Login authentication
    def authenticate(self, request, username=None, password=None):
        try:
            user = DPrevUser.objects.get(username=username)
            password_correct = user.check_password(password)

            # Return user if credentials match
            if (password_correct):
                return user

        except DPrevUser.DoesNotExist:
            pass
        
        # Fail to sign in, credentials not provided
        return None

# Show all game results
class GameResultViewSet(viewsets.ModelViewSet):
    """
    Show game result
    """
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer

# Show all photo name pairs
class PhotoNamePairViewSet(viewsets.ModelViewSet):
    """
    Show photo name pair
    """
    queryset = PhotoNamePair.objects.all()
    serializer_class = PhotoNamePairSerializer

# All games
class GameViewSet(viewsets.ModelViewSet):
    """
    Show games
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

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

# All users
class DPrevUserViewSet(viewsets.ModelViewSet):
    """
    Show users
    """
    queryset = DPrevUser.objects.all()
    serializer_class = DPrevUserSerializer

# Restrict to one user
@csrf_exempt
def user_details(request, pk):
    try:
        user = DPrevUser.objects.get(pk=pk)
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

