from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from paymentapp.models import Checkout

# Create your models here.
class Banner(models.Model):
    title  = models.CharField(max_length = 150)
    image = models.ImageField(upload_to='BannerImage')
    url_http_link = models.URLField(max_length = 300, blank=True, null=True)
    
    class Meta:
        """Meta definition for Banner."""
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length = 150)
    parent_category  = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='child')
    image  = models.ImageField(upload_to='CategoriesImage')
    
    

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length = 150)
    image  = models.ImageField(upload_to='BrandImage')
    
    

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class Product(models.Model):
    name  = models.CharField(max_length = 250)
    image = models.ImageField(upload_to='ProductImage')
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    description  = RichTextField()
    aditional_description = RichTextField()
    stock = models.IntegerField()
    category  = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name + ' / ' + str(self.id)

    def get_review_list(self):
        reviews = ProductReview.objects.filter(product=self,approve_status=True)
        return reviews

    def get_avg_rating(self):
        reviews = ProductReview.objects.filter(product=self,approve_status=True)
        count = len(reviews)
        sum = 0
        for rvw in reviews:
            sum += rvw.rating
        if count != 0:
            return (sum*20/count)

    def get_rating_count(self):
        reviews = ProductReview.objects.filter(product=self,approve_status=True)
        count = len(reviews)
        return count

class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



    def product_subtotal(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        else:
             return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_product = models.ManyToManyField(CartProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address  = models.ForeignKey(Checkout, on_delete=models.CASCADE, blank=True, null=True)
    PAYMENT_METHOD =(
        ('Cash on Delivery','Cash on Delivery'),
        ('Bkash','Bkash')
    )
    payment_option  = models.CharField(max_length = 150, choices=PAYMENT_METHOD, blank=True, null=True)


    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for i in self.cart_product.all():
            total += i.product_subtotal()
        return total


    def get_final_total(self):
        return self.get_total() + 90



class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class AboutABC(models.Model):
    description  = RichTextField(default='xyz')
    
    class Meta:
        verbose_name_plural = 'AboutABC'

    def __str__(self):
        return 'About Us'

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    RATING =(
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )
    rating  = models.IntegerField(choices=RATING, default=5)
    review = models.TextField()
    image = models.ImageField(upload_to='ReviewImg', blank=True, null=True)
    approve_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

