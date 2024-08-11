from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from portal.views import SignupView, LandingView, HomeView, OfferingsListView, OfferingDetailView, CreateRequestAllocationView, CreateReferralView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', LandingView.as_view(), name='landing'),
    path('home/', HomeView.as_view(), name='home'),
    path('offerings/', OfferingsListView.as_view(), name='offerings_list'),
    path('offerings/<slug:slug>/', OfferingDetailView.as_view(), name='offerings_detail'),
    path('create-request-allocation/', CreateRequestAllocationView.as_view(), name='create_request_allocation'),
    path('create-referral/', CreateReferralView.as_view(), name='create_referral'),
]
