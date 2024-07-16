from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import FarmerSignUpForm, ConsumerSignUpForm, LoginForm, FarmForm, eggInventoryForm, ExpenseInventoryForm
from .models import Farm, Farmer, Consumer, eggInventory, expenseInventory,  EggBatch, Order, OrderItem
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.db.models import Sum
from django.db import IntegrityError, transaction

from .forms import OrderForm, OrderItemFormSet
import logging

def home(request):
    return render(request, 'core/home.html')

def farmer_signup(request):
    if request.method == 'POST':
        form = FarmerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = FarmerSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'user_type': 'Farmer'})

def consumer_signup(request):
    if request.method == 'POST':
        form = ConsumerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ConsumerSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'user_type': 'Consumer'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully.')
                return redirect('home')  
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('home')  


def farm_list(request):
    farms = Farm.objects.filter(farmer__user=request.user)
    return render(request, 'core/farm_list.html', {'farms': farms})



class FarmListView(ListView):
    model = Farm
    template_name = 'core/farm_list.html'
    context_object_name = 'farms'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all farms
        farms = Farm.objects.all()

        # Calculate total stock for each farm
        for farm in farms:
            total_stock = eggInventory.objects.filter(farm=farm).aggregate(total_stock=Sum('stock'))['total_stock']
            farm.total_stock = total_stock if total_stock else 0

        context['farms'] = farms
        return context

class FarmDetailView(DetailView):
    model = Farm
    template_name = 'core/farm_detail.html'

    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm = self.get_object()
        egg_inventories = eggInventory.objects.filter(farm=farm)

        total_stock = sum(inventory.stock for inventory in egg_inventories)

        context['egg_inventories'] = egg_inventories
        context['expense_inventories'] = expenseInventory.objects.filter(farm=self.object)
        context['total_stock'] = total_stock
        return context

class FarmCreateView(LoginRequiredMixin,CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'core/farm_form.html'
    success_url = reverse_lazy('farm_list')


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'farmer'):
            return HttpResponseForbidden("You must be a farmer to create a farm.")
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
            user = self.request.user
            if not hasattr(user, 'farmer'):
                return self.handle_no_permission()

            form.instance.farmer = user.farmer
            response = super().form_valid(form)

            eggInventory.objects.create(
                farm=form.instance,
                stock=0,  # Initial stock value, adjust as needed
                trayPrice=0,  # Initial trayPrice value, adjust as needed
                batch_number='default_batch'  # Ensure batch_number has a default value
        )

            return response        
 

class FarmUpdateView(UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = 'core/farm_form.html'
    success_url = reverse_lazy('farm_list')

class FarmDeleteView(DeleteView):
    model = Farm
    template_name = 'core/farm_confirm_delete.html'
    success_url = reverse_lazy('farm_list')




class eggInventoryCreateView(CreateView):
    model = eggInventory
    form_class = eggInventoryForm
    template_name = 'core/egg_inventory_form.html'
    success_url = reverse_lazy('farm_list')  # Adjust as needed

    def form_valid(self, form):
    # Get the farm instance from the URL parameter
        farm_id = self.kwargs['farm']
        farm = get_object_or_404(Farm, pk=farm_id)

        # Assign the farm instance to the form instance
        form.instance.farm = farm

        # Call the parent form_valid method to save the form
        return super().form_valid(form)
    
def create_egg_inventory(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    if request.method == 'POST':
        form = eggInventoryForm(request.POST)
        if form.is_valid():
            egg_inventory = form.save(commit=False)
            egg_inventory.farm = farm
            egg_inventory.batch_number = 'default_batch'  # Ensure batch_number is provided
            egg_inventory.save()
            return redirect(reverse('farm_detail', kwargs={'pk': farm.id}))
    else:
        form = eggInventoryForm()
    return render(request, 'core/create_egg_inventory.html', {'form': form, 'farm': farm})
    
def egg_inventory_list(request):
    egg_inventories = eggInventory.objects.all()

    context = {
        'egg_inventories': egg_inventories,
    }

    return render(request, 'core/egg_inventory_list.html', context)


class ExpenseInventoryCreateView(CreateView):
    model = expenseInventory
    form_class = ExpenseInventoryForm
    template_name = 'core/expense_inventory_form.html'


    def form_valid(self, form):
        form.instance.farm_id = self.kwargs['farm_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('expense_inventory_list')  # redirect to the list view after a successful form submission
    




class ExpenseInventoryUpdateView(UpdateView):
    model = expenseInventory
    form_class = ExpenseInventoryForm
    template_name = 'core/expense_inventory_form.html'
    success_url = reverse_lazy('expense_inventory_list')

class ExpenseInventoryDeleteView(DeleteView):
    model = expenseInventory
    template_name = 'core/expense_inventory_confirm_delete.html'
    success_url = reverse_lazy('expense_inventory_list')

class ExpenseInventoryDetailView(DetailView):
    model = expenseInventory
    template_name = 'core/expense_inventory_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cost'] = self.object.quantity * self.object.unitPrice
        return context

class ExpenseInventoryListView(ListView):
    model = expenseInventory
    template_name = 'core/expense_inventory_list.html'
    context_object_name = 'expense_inventories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

logger = logging.getLogger(__name__)

@login_required
def create_order(request, farm_id):
    if not request.user.is_consumer:
        raise PermissionDenied
    farm = get_object_or_404(Farm, pk=farm_id)
    egg_batches = eggInventory.objects.filter(farm=farm)  

    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.consumer = request.user
                    order.farm = farm
                    order.save()
                    logger.debug(f"Order created: {order}")

                    for item_form in formset:
                        if item_form.cleaned_data:
                            order_item = item_form.save(commit=False)
                            order_item.order = order
                            order_item.save()
                            logger.debug(f"OrderItem created: {order_item}")
                    
                    return redirect('order_detail', order_id=order.id)
            except IntegrityError as e:
                logger.error(f"IntegrityError: {e}")
                form.add_error(None, "There was an issue saving the order. Please try again.")
        else:
            logger.error(f"Form errors: {form.errors}, {formset.errors}")
    else:
        form = OrderForm()
        formset = OrderItemFormSet(queryset=eggInventory.objects.none())

    return render(request, 'core/create_order.html', {'form': form, 'formset': formset, 'farm': farm, 'egg_batches': egg_batches})
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'core/order_detail.html', {'order': order})