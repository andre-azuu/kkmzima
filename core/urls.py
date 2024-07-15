from django.urls import path
from .views import home, farmer_signup, consumer_signup,logout_view,login_view,farm_list
from .views import FarmListView, FarmDetailView, FarmCreateView, FarmUpdateView, FarmDeleteView

urlpatterns = [
    path('', home, name='home'),
    path('signup/farmer/', farmer_signup, name='farmer_signup'),
    path('signup/consumer/', consumer_signup, name='consumer_signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('farms/', farm_list, name='farm_list'),
    path('<int:pk>/', FarmDetailView.as_view(), name='farm_detail'),
    path('create-farm/', FarmCreateView.as_view(), name='farm_create'),
    path('<int:pk>/update/', FarmUpdateView.as_view(), name='farm_update'),
    path('<int:pk>/delete/', FarmDeleteView.as_view(), name='farm_delete'),


]
