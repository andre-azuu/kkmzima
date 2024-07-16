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

from django.db.models import Sum


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

            # Automatically create an eggInventory instance for the new farm
            eggInventory.objects.create(
                farm=form.instance,
                stock=0,  # Initial stock value, adjust as needed
                trayPrice=0  # Initial trayPrice value, adjust as needed
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
    

@login_required
def create_order(request, farm_id):
    if not request.user.is_consumer:
        raise PermissionDenied
    farm = get_object_or_404(Farm, id=farm_id)
    
    if request.method == 'POST':
        order = Order.objects.create(consumer=request.user, farm=farm)
        egg_batch_id = request.POST.get('egg_batch')
        quantity = int(request.POST.get('quantity'))
        egg_batch = get_object_or_404(EggBatch, id=egg_batch_id)
        OrderItem.objects.create(order=order, egg_batch=egg_batch, quantity=quantity)
        return redirect('order_detail', order_id=order.id)
    else:
        egg_batches = EggBatch.objects.filter(farm=farm)
        return render(request, 'core/create_order.html', {'farm': farm, 'egg_batches': egg_batches})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'core/order_detail.html', {'order': order})