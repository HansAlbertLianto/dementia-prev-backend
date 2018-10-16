from dprev_backend.models import GameResult, PhotoNamePair, Game, DPrevUser
from dprev_backend.serializers import GameResultSerializer, PhotoNamePairSerializer, GameSerializer, DPrevUserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Show all game results
class GameResultList(APIView):
    """
    Show game result
    """
    def get(self, request, format=None):
        gameresults = GameResult.objects.all()
        serializer = GameResultSerializer(gameresults, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GameResultSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Show all photo name pairs
class PhotoNamePairList(APIView):
    """
    Show photo name pair
    """
    def get(self, request, format=None):
        photonamepairs = PhotoNamePair.objects.all()
        serializer = PhotoNamePairSerializer(photonamepairs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PhotoNamePairSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# All games
class GameList(APIView):
    """
    Show games
    """
    def get(self, request, format=None):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GameSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# All users
class DPrevUserList(APIView):
    """
    Show users
    """
    def get(self, request, format=None):
        dprevusers = DPrevUser.objects.all()
        serializer = DPrevUserSerializer(dprevusers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DPrevUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
