from django.contrib.auth.models import User, Group
from dprev_backend.models import DPrevUser, Game, GameResult, PhotoNamePair
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

# Shows score results of a particular game
class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = ('player', 'score', 'datetime_reached')

# Shows a link to a photo and a name
class PhotoNamePairSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoNamePair
        fields = ('photo_link', 'name')

# Shows the game, its photo and name pairs, and its score history
class GameSerializer(serializers.ModelSerializer):
    photo_name_pairs = PhotoNamePairSerializer(many=True)
    game_result_history = GameResultSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('photo_name_pairs', 'game_result_history')
    
    # Create a game and its pairs
    def create(self, validated_data):
        photo_name_pairs = validated_data.pop('photo_name_pairs')
        game = Game.objects.create(**validated_data)

        for photo_name_pair in photo_name_pairs:
            PhotoNamePair.objects.create(**photo_name_pair)
        
        return game

# Shows the user, the games made by the user, and the scores the
# user has attained in the games
class DPrevUserSerializer(serializers.ModelSerializer):
    user_result_history = GameResultSerializer(many=True, read_only=True)
    games_made = GameSerializer(many=True)

    class Meta:
        model = DPrevUser
        fields = ('full_name', 'username', 'email', 'games_made', 'user_result_history')