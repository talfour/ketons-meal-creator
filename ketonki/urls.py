from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django_editorjs.views import EditorjsImageUploaderView
from .views import SearchResultView
from .forms import LoginForm
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="home"),
    path('search/', SearchResultView.as_view(), name="search"),

    # AUTHENTICATION
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name="password_change"),
    path('passowrd_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name="password_change_done"),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path('register', views.register, name="register"),
    path('register/confirm', views.register_confirm, name='register_confirm'),
    path("editorjs/image/", EditorjsImageUploaderView.as_view()),
    path('profiles/', include('profiles.urls'), name="profiles"),
    path('questions/', include('questions.urls'), name="questions"),
    path('recipes/', include('recipes.urls'), name="recipes"),
    path('foods/', include('food.urls'), name="food"),
    path('captcha/', include('captcha.urls')),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),

    # API
#     path('v1/api/recipes/', include("recipes.api.urls"), name="recipes-api"),

]
handler404 = views.handler404
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
