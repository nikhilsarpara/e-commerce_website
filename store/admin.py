from django.contrib import admin
from .models import product
# Register your models here.

class adminproduct(admin.ModelAdmin):
    list_display=['product_name']
    prepopulated_fields={'slug':('product_name',)}
admin.site.register(product,adminproduct)