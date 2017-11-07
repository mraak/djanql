from django.contrib import admin
from .models import Product
from orgs.models import Org


# Define the admin class
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'created_date')


    def get_queryset(self, request):
        '''
            This is deprecated and makes users being able to log into admin and see their objects
        '''
        qs = super(ProductAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        userOrg = Org.objects.filter(admin=request.user).first()
        return qs.filter(org=userOrg)


# Register the admin class with the associated model
admin.site.register(Product, ProductAdmin)
