from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from dprev_backend.models import GameResult, PhotoNamePair, Game, DPrevUser
from dprev_backend.serializers import UserSerializer, GroupSerializer, GameResultSerializer, PhotoNamePairSerializer, GameSerializer, DPrevUserSerializer

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

class GameResultViewSet(viewsets.ModelViewSet):
    """
    Show game result
    """
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer

class PhotoNamePairViewSet(viewsets.ModelViewSet):
    """
    Show game result
    """
    queryset = PhotoNamePair.objects.all()
    serializer_class = PhotoNamePairSerializer

class GameViewSet(viewsets.ModelViewSet):
    """
    Show game result
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class DPrevUserViewSet(viewsets.ModelViewSet):
    """
    Show game result
    """
    queryset = DPrevUser.objects.all()
    serializer_class = DPrevUserSerializer


