import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .models import RequestAllocation, Offering, User, Referral

class SignupView(View):
    template_name = 'signup.html'
    
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class LandingView(TemplateView):
    template_name = 'landing.html'

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_id'] = user.id
        context['username'] = f"{user.first_name} {user.last_name}"
        context['phone_number'] = user.phone_number
        context['country_of_residence'] = user.country_of_residence
        context['investor_types'] = user.investor_types.all()
        context['offerings'] = Offering.objects.filter(
            is_active=True,
            investor_types__in=context['investor_types']
        ).distinct().order_by('-start_date')
        context['req_allocations'] = RequestAllocation.objects.filter(user=user)
        return context

class OfferingsListView(LoginRequiredMixin, ListView):
    template_name = 'offerings/offerings_list.html'
    context_object_name = 'offerings'

    def get_queryset(self):
        user_investor_types = self.request.user.investor_types.all()
        return Offering.objects.filter(
            is_active=True,
            investor_types__in=user_investor_types
        ).distinct().order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_investor_types = self.request.user.investor_types.all()
        context['past_offerings'] = Offering.objects.filter(
            is_active=False,
            investor_types__in=user_investor_types
        ).distinct().order_by('-end_date')
        return context

class OfferingDetailView(LoginRequiredMixin, DetailView):
    model = Offering
    template_name = 'offerings/offerings_detail.html'
    context_object_name = 'offering'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.investor_types.filter(id__in=self.request.user.investor_types.all()).exists():
            redirect('offerings_list')
        return obj

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

class CreateReferralView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data.get('user')
        print(data)
        invite_name = data.get('invite_name')
        invite_email = data.get('invite_email')

        try:
            user = User.objects.get(pk=user_id)
            referral = Referral.objects.create(
                user=user,
                invite_name=invite_name,
                invite_email=invite_email
            )

            return JsonResponse({'status': 'success', 'data': {'id': referral.id}})
        
        except (User.DoesNotExist, ValueError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
