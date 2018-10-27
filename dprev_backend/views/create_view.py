from dprev_backend.models import ShuffledGame, Game, PhotoNameQuestion, PhotoNamePair
from dprev_backend.serializers import ShuffledGameSerializer
from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
import random, math
import base64

# Create a new instance of shuffled game
def createNewShuffledGame(request, gamename):
    if (request.method == 'POST'):
        try:
            game = Game.objects.get(gamename=gamename)
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

            corresponding_photo = PhotoNamePair.objects.get(name = photo_names[index])

            question = PhotoNameQuestion.objects.create(game_with_photo=shuffled_game, corresponding_photo=corresponding_photo, name=shuffled_photo_names[index], correct=correct)
            question.save()

# Create default game
def createNewDefaultGame(request, gamename):
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

    shuffled_game = ShuffledGame.objects.create(base_game=Game.objects.get(gamename=gamename))
    shuffled_game.save()

    for index in range(0, len(photo_names)):
        if photo_names[index] == shuffled_photo_names[index]:
            correct = True
        else:
            correct = False

        question = PhotoNameQuestion.objects.create(game_with_photo=shuffled_game, default_photo_link = photo_links[index], name=shuffled_photo_names[index], correct=correct)
        question.save()

# Create new game with images
def createNewGame(request):
    if (request.method == 'POST'):
        try:
            user = request.POST.get("user")
            new_game = Game.objects.create(creator=user)
            new_game.save()

            counter = 0

            for str, img_name in request.POST.get("game_image_list"):
                counter += 1

                if (counter > 10):
                    break

                # Try to decode the base64 string and place it in image or file field
                format, imgstr = str.split(';base64,') 
                ext = format.split('/')[-1] 
                data = ContentFile(base64.b64decode(imgstr))
                filename = new_game.creator + "-" + new_game.id + "-" + str(counter) + ext
                
                photo = PhotoNamePair.objects.create(game_with_photo=new_game, photo_link=filename, name=img_name)

        except:
            print("Image save error!")
            
            

