from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from dprev_backend.models import GameResult, PhotoNamePair, Game, DPrevUser
from dprev_backend.serializers import UserSerializer, GameResultSerializer, PhotoNamePairSerializer, GameSerializer, DPrevUserSerializer, ShuffledGameSerializer, PhotoNameQuestionSerializer
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
import random, math

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer