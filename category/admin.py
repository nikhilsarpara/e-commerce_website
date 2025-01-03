from django.contrib import admin
from category.models import category
# Register your models here.

class categoryadmin(admin.ModelAdmin):
    list_display=['category_name']
    prepopulated_fields={'slug':('category_name',)}
admin.site.register(category,categoryadmin)