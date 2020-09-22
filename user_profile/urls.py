from django.urls import path

from user_profile import views

urlpatterns = [
    path('profile/show',views.show),
    path('profile/update',views.update),
]