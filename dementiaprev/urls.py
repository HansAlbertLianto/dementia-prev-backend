"""dementiaprev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django.views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from dprev_backend.views import api_view, create_view, login_view, restrict_view, views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view.do_login),
    path('signup/', login_view.do_signup),
    path('creategame/', create_view.createNewGame),
    path('createdefault/', create_view.createNewDefaultGame),
    path('dprevusers/<slug:gamename>/', restrict_view.user_details),
    path('games/<slug:gamename>/', restrict_view.shuffledgame_details),
    path('games/<slug:gamename>/create', create_view.createNewShuffledGame),
    path('games/<slug:gamename>/dcreate', create_view.createNewDefaultGame),
    path('gameresults/', api_view.GameResultList.as_view()),
    path('photonamepairs/', api_view.PhotoNamePairList.as_view()),
    path('games/', api_view.GameList.as_view()),
    path('dprevusers/', api_view.DPrevUserList.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^static/(.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT}),
]