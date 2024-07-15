from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import FarmerSignUpForm, ConsumerSignUpForm, LoginForm, FarmForm
from .models import Farm, Farmer, Consumer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden


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
                return redirect('home')  # Replace 'home' with your desired redirect URL after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your home view or any other URL



def farm_list(request):
    farms = Farm.objects.filter(farmer__user=request.user)
    return render(request, 'core/farm_list.html', {'farms': farms})

class FarmListView(ListView):
    model = Farm
    template_name = 'core/farm_list.html'
    context_object_name = 'farms'

class FarmDetailView(DetailView):
    model = Farm
    template_name = 'core/farm_detail.html'

class FarmCreateView(CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'core/farm_form.html'
    success_url = reverse_lazy('farm_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'farmer'):
            return HttpResponseForbidden("You must be a farmer to create a farm.")
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        # Set the farmer field to the authenticated user
        form.instance.farmer = Farmer.objects.get(user=self.request.user)
        return super().form_valid(form)

class FarmUpdateView(UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = 'core/farm_form.html'
    success_url = reverse_lazy('farm_list')

class FarmDeleteView(DeleteView):
    model = Farm
    template_name = 'core/farm_confirm_delete.html'
    success_url = reverse_lazy('farm_list')