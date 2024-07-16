from django.urls import path
from . import views
from .views import home, farmer_signup, consumer_signup,logout_view,login_view,farm_list, egg_inventory_list
from .views import (
    FarmListView, 
    FarmDetailView, 
    FarmCreateView, 
    FarmUpdateView, 
    FarmDeleteView, 
    eggInventoryCreateView,
    ExpenseInventoryCreateView,
    ExpenseInventoryUpdateView,
    ExpenseInventoryDeleteView,
    ExpenseInventoryDetailView,
    ExpenseInventoryListView,
    )

urlpatterns = [
    path('', home, name='home'),
    path('signup/farmer/', farmer_signup, name='farmer_signup'),
    path('signup/consumer/', consumer_signup, name='consumer_signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('farms/', farm_list, name='farm_list'),
    path('farms/<int:pk>/', FarmDetailView.as_view(), name='farm_detail'),
    path('create-farm/', FarmCreateView.as_view(), name='farm_create'),
    path('<int:pk>/update/', FarmUpdateView.as_view(), name='farm_update'),
    path('<int:pk>/delete/', FarmDeleteView.as_view(), name='farm_delete'),

    path('create-egg-inventory/<int:farm>/', eggInventoryCreateView.as_view(), name='create_egg_inventory'),
    path('egg-inventory-list/', egg_inventory_list, name='egg_inventory_list'),

    path('expense-inventory/new/<int:farm_id>/', ExpenseInventoryCreateView.as_view(), name='expense_inventory_new'),
    path('expense-inventory/<int:pk>/edit/', ExpenseInventoryUpdateView.as_view(), name='expense_inventory_edit'),
    path('expense-inventory/<int:pk>/delete/', ExpenseInventoryDeleteView.as_view(), name='expense_inventory_delete'),
    path('expense-inventory/<int:pk>/', ExpenseInventoryDetailView.as_view(), name='expense_inventory_detail'),
    path('expense-inventory/', ExpenseInventoryListView.as_view(), name='expense_inventory_list'),

    path('orders/new/<int:farm_id>/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

]
