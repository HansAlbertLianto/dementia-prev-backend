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

# Login authentication
def do_login(self, request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # Return user if credentials match
        if (user is not None):
            login(request, user)
            return user
        
        # Fail to sign in, credentials not provided
        return None

# Signing up
def do_signup(self, request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        # Check if username already exists. Then check if confirm password matches with password.
        if User.objects.filter(username=username).exists():
            return None
        else:
            if password != confirm_password:
                return None
            user = User.objects.create_user(username, None, password)
            user.save()

            full_name = request.POST['full_name']
            email = request.POST['email']
            
            dprevuser = DPrevUser.objects.create_dprevuser(user, full_name, email)
            dprevuser.save()

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

# Get one game instance
def shuffledgame_details(request, pk, pk2):

    game = Game.objects.get(pk=pk)
    shuffled_game = game.game_instances.get(pk=pk2)

    serializer = ShuffledGameSerializer(shuffled_game)

    return JsonResponse(serializer.data)

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

# Create a new instance of shuffled game
def createNewShuffledGame(request, pk):
    if (request.method == 'POST'):
        try:
            game = Game.objects.get(pk=pk)
        except:
            print("Error!")

        # Extract links and names; need to check if correct or not
        photo_links = game.photo_name_pairs.values_list('photo_link', flat=True)
        photo_names = game.photo_name_pairs.values_list('photo_names', flat=True)

        # Create duplicate list about to be shuffled
        shuffled_photo_names = photo_names.copy()

        # Initialize a random value of swaps
        noOfSwaps = random.randint(1, len(photo_names) // 2)

        # Perform swapping
        for swapNo in range(0, noOfSwaps):
            firstIndex = random.randint(0, len(photo_names) - 1)
            secondIndex = random.randint(0, len(photo_names) - 1)
            shuffled_photo_names[firstIndex], shuffled_photo_names[secondIndex] = shuffled_photo_names[secondIndex], shuffled_photo_names[firstIndex]

        # Create new shuffled game instance
        shuffled_game = ShuffledGame.objects.create(base_game=pk)
        shuffled_game.save()

        # Put photo pair questions
        for index in range(0, len(photo_names)):
            if photo_names[index] == shuffled_photo_names[index]:
                correct = True
            else:
                correct = False

            question = PhotoNameQuestion.objects.create(game_with_photo=shuffled_game.id, photo_link=photo_links[index], photo_names=shuffled_photo_names[index], correct=correct)
            question.save()

# Create default game
def createNewDefaultGame(request, pk):
    photo_links = ["https://upload.wikimedia.org/wikipedia/commons/f/f3/Al_Capone_in_1930.jpg",\
    "https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTE5NTU2MzE2MzIyMTA0ODQz/marilyn-monroe-9412123-1-402.jpg",\
    "https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTE4MDAzNDEwNzg5ODI4MTEw/barack-obama-12782369-1-402.jpg",\
    "https://upload.wikimedia.org/wikipedia/commons/4/43/Omar_Sharif_2015.jpg",\
    "https://cps-static.rovicorp.com/3/JPG_400/MI0003/146/MI0003146038.jpg"]

    photo_names = ["Al Capone",\
    "Marilyn Monroe",\
    "Barack Obama",\
    "Omar Sharif",\
    "Bob Marley"]

    # Create duplicate list about to be shuffled
    shuffled_photo_names = photo_names.copy()

    # Initialize a random value of swaps
    noOfSwaps = random.randint(1, math.ceil(len(photo_names) / 2))

    for swapNo in range(0, noOfSwaps):
        firstIndex = random.randint(0, len(photo_names) - 1)
        secondIndex = random.randint(0, len(photo_names) - 1)
        shuffled_photo_names[firstIndex], shuffled_photo_names[secondIndex] = shuffled_photo_names[secondIndex], shuffled_photo_names[firstIndex]

    shuffled_game = ShuffledGame.objects.create(base_game=pk)
    shuffled_game.save()

    for index in range(0, len(photo_names)):
        if photo_names[index] == shuffled_photo_names[index]:
            correct = True
        else:
            correct = False

        question = PhotoNameQuestion.objects.create(game_with_photo=shuffled_game.id, photo_link=photo_links[index], photo_names=shuffled_photo_names[index], correct=correct)
        question.save()