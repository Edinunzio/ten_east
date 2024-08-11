import json
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views import View
from django.http import JsonResponse
from .models import RequestAllocation, Offering, User

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def landing(request):
    return render(request, 'landing.html')

@login_required
def home(request):
    user = request.user
    phone_number = user.phone_number
    country_of_residence = user.country_of_residence
    user_investor_types = request.user.investor_types.all()
    active_offerings = Offering.objects.filter(
        is_active=True,
        investor_types__in=user_investor_types
    ).distinct().order_by('-start_date')
    req_allocations = RequestAllocation.objects.filter(
        user=user
    )
    return render(request, 'home.html', {
        'offerings': active_offerings,
        'req_allocations': req_allocations,
        'username': (user.first_name + ' ' + user.last_name),
        'phone_number': phone_number,
        'country_of_residence': country_of_residence,
        'investor_types': user_investor_types
    })

@login_required
def offerings_list(request):
    user_investor_types = request.user.investor_types.all()
    offerings = Offering.objects.filter(
        is_active=True,
        investor_types__in=user_investor_types
    ).distinct().order_by('-start_date')
    past_offerings = Offering.objects.filter(
        is_active=False,
        investor_types__in=user_investor_types
    ).distinct().order_by('-end_date')

    return render(request, 'offerings/offerings_list.html', {
        'offerings': offerings,
        'past_offerings': past_offerings
    })

@login_required
def offerings_detail(request, slug):
    offering = get_object_or_404(Offering, slug=slug, is_active=True)
    
    if not offering.investor_types.filter(id__in=request.user.investor_types.all()).exists():
        return redirect('offerings_list')
    
    return render(request, 'offerings/offerings_detail.html', {
        'offering': offering
    })

class CreateRequestAllocationView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data.get('user')
        offering_id = data.get('offering')
        amount = data.get('amount')

        try:
            user = User.objects.get(pk=user_id)
            offering = Offering.objects.get(pk=offering_id)
            amount = float(amount)

            request_allocation = RequestAllocation.objects.create(
                user=user,
                offering=offering,
                amount=amount
            )

            return JsonResponse({'status': 'success', 'data': {'id': request_allocation.id}})
        
        except (User.DoesNotExist, Offering.DoesNotExist, ValueError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)})