from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Offering

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Adjust to your desired redirect after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def landing(request):
    return render(request, 'home.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def offerings_list(request):
    user_investor_types = request.user.investor_types.all()
    offerings = Offering.objects.filter(
        is_active=True,
        investor_types__in=user_investors_types
    ).distinct().order_by('-start_date')

    return render(request, 'offerings/offerings_list.html', {
        'offerings': offerings
    })

@login_required
def offering_detail(request, offering_id):
    offering = get_object_or_404(Offering, id=offering_id, is_active=True)
    
    if not offering.investor_types.filter(id__in=request.user.investor_types.all()).exists():
        return redirect('offerings_list')
    
    return render(request, 'offerings/offering_detail.html', {
        'offering': offering
    })