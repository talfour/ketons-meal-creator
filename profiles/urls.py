from django.urls import path
from django.urls import path, register_converter
from datetime import datetime
from .views import (ProfileDetailView,
                    ProfileListView,
                    add_new_meal_to_day,
                    delete_meal_from_day,
                    following_users_list,
                    my_profile_view,
                    user_follow,
                    user_calendar,
                    calendar_day_details)

app_name = 'profiles'


class DateConverter:
    regex = '\d{4}\d{2}\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y%m%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('myprofile/', my_profile_view, name="my-profile-view"),
    path('following/', following_users_list, name="following"),
    path('profile-list/', ProfileListView.as_view(), name="profile-list"),
    path('profile/follow_user/', user_follow, name="user-follow"),
    path('profile-details/<slug>',
         ProfileDetailView.as_view(), name='profile-details'),
    path('myprofile/calendar/', user_calendar, name="calendar"),
    path('myprofile/calendar-detail/<yyyy:date>',
         calendar_day_details, name="calendar-detail"),
    path('myprofile/add-new-meal/', add_new_meal_to_day, name='calendar-new-meal'),
    path('myprofile/delete-meal/<pk>',
         delete_meal_from_day, name="calendar-delete-meal"),
]
