from django.contrib import admin
from .models import User, Offering, OfferingTag, InvestorType, \
      RequestAllocation, Referral


class OfferingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'start_date',
        'end_date',
        'is_active',
        'display_investor_types',
        )
    
    def display_investor_types(self, obj):
        return ", ".join(
            [investor_type.name for investor_type in obj.investor_types.all()]
            )
    display_investor_types.short_description = 'Investor Types'


admin.site.register(User)
admin.site.register(Offering, OfferingAdmin)
admin.site.register(OfferingTag)
admin.site.register(InvestorType)
admin.site.register(RequestAllocation)
admin.site.register(Referral)
