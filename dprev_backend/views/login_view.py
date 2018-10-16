from django.contrib.auth.models import User
from dprev_backend.models import DPrevUser
from django.contrib.auth import login, authenticate

# Create views here

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