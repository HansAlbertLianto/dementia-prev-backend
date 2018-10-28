from django.test import TestCase
from django.utils import timezone
from dprev_backend.models import DPrevUserManager

# Create your tests here.
class DPrevUserManagerTestCase(TestCase):
    def create_DPrevUserManager(self):
        return self.objects.create(user=user, full_name='Alice', email='testing@example.com')
  

    def test_create_dprevuser(self):
        user = self.create_DPrevUserManager()
        self.assertTrue(isinstance(user, DPrevUserManager))

class DPrevUserTestCase(TestCase):
    def setUp(cls):
        DPrevUser.objects.create(user=user, full_name='Alice', email='testing@example.com')

    def test_DPrevUser_fullname_label(self):
        user = DPrevUser.objects.get(1)
        name_field = user._meta.get_field('full_name').verbose_name
        self.assertEquals(name_field, 'Alice')

    def test_DPrevUser_email_label(self):
        user = DPrevUser.objects.get(1)
        email_field = user._meta.get_field('email').verbose_name
        self.assertEquals(name_field, 'testing@example.com')

class GameTestCase(TestCase):
    def setUp():
        DPrevUser.objects.create(user=user, full_name='Alice', email='testing@example.com')
        Game.objects.create(creator = DPrevUser.objects.get(1), gamename = 'something')

    def test_Game_creator_label(self):
        game = Game.objects.get(1)
        creator_field = game._meta.get_field('creator').verbose_name
        self.assertEquals(creator_field, DPrevUser.objects.get(1))

    def test_Game_gamename_label(self):
        game = Game.objects.get(1)
        game_field = game._meta.get_field('gamename').verbose_name
        self.assertEquals(game_field, 'something')
        
class GameResultTestCase(TsetCase):
    def setUp():
        DPrevUser.objects.create(user=user, full_name='Alice', email='testing@example.com')
        Game.objects.create(creator = DPrevUser.objects.get(1), gamename = 'something')
        ShuffleGame.objects.create(Game.objects.get(1))
        GameResult.objects.create(player = DPrevUser.objects.get(1), game_instance_played = ShuffleGame.objects.get(1),game_played = Game.objects.get(1), score = '10', datetime_reached =  timezone.now())

    def test_gameresult_creation(self):
        game_result = GameResult.objects.get(1)
        self.assertTrue(isinstance(game_result, GameResult))

class PhotoNamePairTestCase(TestCase):
    def setUp(self):
        DPrevUser.objects.create(user=user, full_name='Alice', email='testing@example.com')
        Game.objects.create(creator = DPrevUser.objects.get(1), gamename = 'something')
        PhotoNamePair.objects.create(game_with_photo = Game.objects.get(1), photo_link = 'photos', name = 'Bob')

    def test_PhotoNamePair_creation(self):
        photonamepair = PhotoNamePair.objects.get(1)
        self.assertTrue(isinstance(photonamepair, PhotoNamePair))

class PhotoNameQuestionTestCase(TestCase):
    def setup(self):
        DPrevUser.objects.create(user=user, full_name='Alice', email='testing@example.com')
        Game.objects.create(creator = DPrevUser.objects.get(1), gamename = 'something')
        PhotoNamePair.objects.create(game_with_photo = Game.objects.get(1), photo_link = 'photos', name = 'Bob')
        PhotoNameQuestion.objects.create(game_with_photo = Game.objects.get(1), corresponding_photo = PhotoNamePair.objects.get(1), default_photo_link = 'photos', name = 'Chuck', correct = False)

    def test_PhotoNameQuestion_creation(self):
        photogamequestion = PhotoNameQuestion.objects.get(1)
        self.assertTrue(isinstance(photogamequestion, PhotoNameQuestion))


