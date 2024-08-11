from django.contrib import admin
from .models import User, Offering, OfferingTag, InvestorType, RequestAllocation

admin.site.register(User)
admin.site.register(Offering)
admin.site.register(OfferingTag)
admin.site.register(InvestorType)
admin.site.register(RequestAllocation)
