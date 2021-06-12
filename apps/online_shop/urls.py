from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('filter/<int:category_id>', views.ProductListView.as_view(), name='filter'),
    path('search', views.ProductListView.as_view(), name='search'),
    path('show/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('review/<int:pk>', views.ProductReviewView.as_view(), name='show_review'),
    path('cart', views.CartView.as_view(), name='show_cart'),
    path('cart/update_item', views.update_item_inCart, name='update_item_inCart'),
    path('cart/delete_item/<int:item_id>', views.delete_item_fromCart, name='delete_item_fromCart'),
    path('checkout', views.checkout, name='checkout'),
    path('order_complete', views.OrderCompleteView.as_view(), name='order_complete'),
    path('dashboard', views.AdminOrderListView.as_view(), name='dashboard'),
    path('orders/search', views.AdminOrderListView.as_view(), name='order_search'),
    path('orders/show/<int:pk>', views.AdminOrderDetailView.as_view(), name='admin_order_detail'),
    path('orders/update_status', views.update_status, name='update_status'),
    path('dashboard/products', views.AdminProductListView.as_view(), name='dashboard_products'),
    path('products/search', views.AdminProductListView.as_view(), name='product_search'),
    path('products/add_new', views.add_product, name='add_product'),
    path('products/update/<int:pk>', views.update_product, name='update_product'),
    path('products/delete/<int:pk>', views.delete_product, name='delete_product'),
    path('images/delete/<int:pk>/<place>', views.delete_image, name='delete_image'),
    path('categories/remove/<int:product_pk>/<int:category_pk>', views.remove_category, name='remove_category'),
]
