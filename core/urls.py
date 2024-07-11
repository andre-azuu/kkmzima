from django.urls import path
from .views import home, farmer_signup, consumer_signup,logout_view,login_view

urlpatterns = [
    path('', home, name='home'),
    path('signup/farmer/', farmer_signup, name='farmer_signup'),
    path('signup/consumer/', consumer_signup, name='consumer_signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
