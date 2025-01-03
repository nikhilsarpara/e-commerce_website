from django.db import models
from category.models import category
from django.urls import reverse
# Create your models here.

class product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    product_detail = models.CharField(max_length=200)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    product_price = models.IntegerField()
    product_stock = models.IntegerField()
    product_image = models.ImageField(upload_to='product_image/')
    product_discription=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])