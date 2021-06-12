from django.db import models
from ..register_login_app.models import CustomUser
from django.core import validators

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    description = models.TextField(max_length=1000)
    main_image = models.ImageField(upload_to='img')
    categories = models.ManyToManyField(Category, related_name='products')
    sold = models.IntegerField(default=0)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='img')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image_Product#{self.product.id}'
    
class ProductReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='reviews')
    content = models.TextField(validators=[validators.MinLengthValidator(15, 'Please enter at least 15 charactors')])
    star = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Review#{self.id}'

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_cost = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart#{self.id}'

class ProductCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    qty = models.IntegerField()
    cost = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ProductInCart#{self.cart.id}'

STATUS_CHOICES = (('Received', 'Received'), ('Shipped', 'Shipped'), ('In Progress', 'In Progress'), ('Cancelled', 'Cancelled'))

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="In Progress")
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order#{self.id}'

    def get_total(self):
        grand_total = self.shipping_cost + self.cart.total_cost
        return grand_total

class ShippingInfo(models.Model):
    first_name = models.CharField(max_length=45, validators=[validators.MinLengthValidator(2, 'Please make at least 2 charactors')])
    last_name = models.CharField(max_length=100, validators=[validators.MinLengthValidator(2, 'Please make at least 2 charactors')])
    address = models.CharField(max_length=500)    
    address2 = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return f'Shipping_{self.first_name}_{self.last_name}'

class BillingInfo(models.Model):
    first_name = models.CharField(max_length=45, validators=[validators.MinLengthValidator(2, 'Please make at least 2 charactors')])
    last_name = models.CharField(max_length=100, validators=[validators.MinLengthValidator(2, 'Please make at least 2 charactors')])
    address = models.CharField(max_length=500)    
    address2 = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    card_number = models.IntegerField()
    card_security = models.IntegerField()
    expiration = models.CharField(max_length=10)

    def __str__(self):
        return f'Billing_{self.first_name}_{self.last_name}'

class Payment(models.Model):
    shipping_info = models.ForeignKey(ShippingInfo, on_delete=models.CASCADE)
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return f'Payment#{self.id}'