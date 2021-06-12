from django.contrib import admin
from .models import Product, Order, Category, Payment, ShippingInfo, BillingInfo, ProductImage

class ProductAdmin(admin.ModelAdmin):
    pass
class OrderAdmin(admin.ModelAdmin):
    pass
class CategoryAdmin(admin.ModelAdmin):
    pass
class PaymentAdmin(admin.ModelAdmin):
    pass
class ShippingAdmin(admin.ModelAdmin):
    pass
class BillingAdmin(admin.ModelAdmin):
    pass
class ProductImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ShippingInfo, ShippingAdmin)
admin.site.register(BillingInfo, BillingAdmin)
admin.site.register(ProductImage, ProductImageAdmin)