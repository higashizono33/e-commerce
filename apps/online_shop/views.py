from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.core.paginator import Paginator
from .models import Product, Order, Category, Cart, ProductCart, Payment, STATUS_CHOICES, ProductImage, ProductReview
from ..register_login_app.models import CustomUser
from django.template.defaulttags import register
from django.http import JsonResponse
from .forms import ShippingForm, BillingForm, ReviewForm
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import copy

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class ProductListView(ListView):
    paginate_by = 6
    template_name = 'index.html'

    def get_queryset(self):
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            queryset = Product.objects.filter(name__contains=keyword)
        elif 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']
            queryset = Product.objects.filter(categories=category_id)
        else:
            queryset = Product.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        context['counts'] = {}
        for category in Category.objects.all():
            temp_dict = {f'{category.name}': Product.objects.filter(categories=category.id).count()}
            context['counts'].update(temp_dict)
        if 'cartId' in self.request.session:
            context['item_count'] = ProductCart.objects.filter(cart=self.request.session['cartId']).count()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Product.objects.get(id=self.kwargs['pk']).categories.all()
        context['images'] = ProductImage.objects.filter(product=self.kwargs['pk'])
        context['similar_products'] = []
        for category in categories:
            similar_products = Category.objects.get(name=category).products.all()
            for similar_product in similar_products:
                context['similar_products'].append(similar_product)
        if 'cartId' in self.request.session:
            context['item_count'] = ProductCart.objects.filter(cart=self.request.session['cartId']).count()
        context['price_qty'] = []
        product = Product.objects.get(id=self.kwargs['pk'])
        for i in range(1,6):
            temp_dict = {'qty': i, 'price': i * product.price}
            context['price_qty'].append(temp_dict)
        return context
    
    def post(self, request, *args, **kwargs):
        current_user = CustomUser.objects.get(id=self.request.session['userId'])
        if not 'cartId' in self.request.session:
            new_cart = Cart.objects.create(user=current_user, total_cost=0)
            self.request.session['cartId'] = new_cart.id
        current_product = Product.objects.get(id=self.kwargs['pk'])
        current_cart = Cart.objects.get(id=self.request.session['cartId'])
        ProductCart.objects.create(
            product=current_product,
            cart=current_cart,
            qty=int(request.POST['qty']),
            cost=current_product.price * int(request.POST['qty'])
        )
        update_total = current_cart.total_cost + (current_product.price * int(request.POST['qty']))
        current_cart.total_cost = update_total
        current_cart.save()
        item_count = ProductCart.objects.filter(cart=self.request.session['cartId']).count()
        return JsonResponse({'item_count': item_count})

def get_sub_total(current_cart):
    items = ProductCart.objects.filter(cart=current_cart)
    sub_total = 0
    for item in items:
        sub_total += item.product.price * item.qty
    return sub_total

def make_shipping_cost(request, sub_total):
    if sub_total >= 35:
        shipping_cost = 0
    else:
        items = ProductCart.objects.filter(cart=request.session['cartId'])
        total_qty = 0
        for item in items:
            total_qty += item.qty
        shipping_cost = round(3.99 * total_qty, 2)
    request.session['shipping_cost'] = shipping_cost
    return shipping_cost

class ProductReviewView(LoginRequiredMixin, ListView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = ProductReview
    template_name = 'review.html'

    def get_queryset(self, **kwargs):
        current_product = Product.objects.get(id=self.kwargs['pk'])
        queryset = ProductReview.objects.filter(products=current_product)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        context['product'] = Product.objects.get(id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        current_user = CustomUser.objects.get(id=self.request.session['userId'])
        form = ReviewForm(self.request.POST)
        current_product = Product.objects.get(id=self.kwargs['pk'])
        queryset = ProductReview.objects.filter(products=current_product)
        if form.is_valid():
            new_review = ProductReview.objects.create(
                user=current_user,
                content=request.POST['content'],
                star=request.POST['star'],
            )
            new_review.products.add(current_product)
            new_review.save()
            return redirect('show_review', pk=self.kwargs['pk'])
        else:
            context = {
                'form': form,
                'product': current_product,
                'object_list': queryset,
            }
            return render(self.request, 'review.html', context)

class CartView(LoginRequiredMixin, TemplateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s_form'] = ShippingForm()
        context['b_form'] = BillingForm()
        if 'cartId' in self.request.session:
            items = ProductCart.objects.filter(cart=self.request.session['cartId'])
            context['items'] = items
            context['item_count'] = ProductCart.objects.filter(cart=self.request.session['cartId']).count()
        else:
            current_user = CustomUser.objects.get(id=self.request.session['userId'])
            new_cart = Cart.objects.create(user=current_user, total_cost=0)
            self.request.session['cartId'] = new_cart.id
        
        current_cart = Cart.objects.get(id=self.request.session['cartId'])
        context['cart'] = current_cart
        shipping_cost = make_shipping_cost(self.request, current_cart.total_cost)
        
        context['total'] = round(float(current_cart.total_cost) + shipping_cost, 2)
        return context

def update_item_inCart(request):
    if request.method == 'GET':
        itemId = int(request.GET['item_id'])
        update_item = ProductCart.objects.get(id=itemId)
        update_item.qty = int(request.GET['qty'])
        update_item.cost = update_item.product.price * update_item.qty
        update_item.save()
        
        current_cart = Cart.objects.get(id=request.session['cartId'])
        sub_total = get_sub_total(current_cart)
        current_cart.total_cost = sub_total
        current_cart.save()

        shipping_cost = make_shipping_cost(request, sub_total)

        context = {
            'cost': update_item.cost,
            'sub_total': round(sub_total, 2),
            'shipping_cost': shipping_cost,
            'total': round(float(sub_total) + shipping_cost, 2),
        }
        return JsonResponse(context)

def delete_item_fromCart(request, item_id):
    delete_item = ProductCart.objects.get(id=item_id)
    delete_item.delete()
    current_cart = Cart.objects.get(id=request.session['cartId'])
    sub_total = get_sub_total(current_cart)
    current_cart.total_cost = sub_total
    current_cart.save()

    shipping_cost = make_shipping_cost(request, sub_total)
    
    items = ProductCart.objects.filter(cart=request.session['cartId'])
    context = {'items': items} 
    table = render_to_string('partial/table.html', context, request=request)
    data = {
        'sub_total': round(sub_total, 2),
        'shipping_cost': shipping_cost,
        'total': round(float(sub_total) + shipping_cost, 2),
        'table': table,
        'item_count': ProductCart.objects.filter(cart=request.session['cartId']).count()
    }
    if request.is_ajax():
        return JsonResponse(data)
    return redirect('show_cart')

def checkout(request):
    if request.method == 'POST':
        s_form = ShippingForm(request.POST)
        b_form = BillingForm(request.POST)
        if s_form.is_valid() and b_form.is_valid():
            current_cart = Cart.objects.get(id=request.session['cartId'])
            new_order = Order.objects.create(
                cart=current_cart,
                shipping_cost=request.session['shipping_cost'],
            )
            new_shipping = s_form.save()
            new_billing = b_form.save()
            new_payment = Payment.objects.create(
                shipping_info=new_shipping,
                billing_info=new_billing,
                order=new_order,
            )
            request.session.pop('cartId', None)
            return redirect('order_complete')
        else:
            context = {
                's_form': s_form,
                'b_form': b_form,
            }
    return render(request, 'checkout.html', context=context)

class OrderCompleteView(TemplateView):
    template_name = "order_complete.html"

class AdminOrderListView(ListView):
    paginate_by = 5
    model = Order
    template_name = 'admin/dashboard.html'
    ordering = ['-id']

    def get_queryset(self):
        if 'keyword' in self.request.GET:
            if self.request.GET['keyword'] != '':
                keyword = self.request.GET['keyword']
                if keyword.isnumeric():
                    queryset = Order.objects.filter(id=keyword)
                else:
                    users = CustomUser.objects.filter(first_name__contains=keyword)
                    carts = []
                    for user in users:
                        user_carts = Cart.objects.filter(user=user).order_by('-id')
                        for user_cart in user_carts:
                            carts.append(user_cart)
                    queryset = []
                    for cart in carts:
                        user_orders = Order.objects.filter(cart=cart).order_by('-id')
                        for user_order in user_orders:
                            queryset.append(user_order)
            else:
                queryset = Order.objects.all().order_by('-id')
        else:
            queryset = Order.objects.all().order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = STATUS_CHOICES
        context['payments'] = Payment.objects.all()
        return context

def update_status(request):
    if request.method == 'GET':
        orderId = int(request.GET['order_id'])
        update_order = Order.objects.get(id=orderId)
        update_order.status = request.GET['status']
        update_order.save()
    return HttpResponse('')

class AdminOrderDetailView(DetailView):
    model = Order
    template_name = 'admin/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        if len(Payment.objects.filter(order=self.object.id)) > 0:
            context['payment'] = Payment.objects.filter(order=self.object.id)[0]
        context['items'] = ProductCart.objects.filter(cart=self.object.cart)
        return context

class AdminProductListView(ListView):
    paginate_by = 5
    model = Product
    template_name = 'admin/product_list.html'
    ordering = ['id']

    def get_queryset(self):
        if 'keyword' in self.request.GET:
            if self.request.GET['keyword'] != '':
                keyword = self.request.GET['keyword']
                if keyword.isnumeric():
                    queryset = Product.objects.filter(id=keyword)
                else:
                    queryset = Product.objects.filter(name__contains=keyword)
            else:
                queryset = Product.objects.all()
        else:
            queryset = Product.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['sub_images'] = ProductImage.objects.all()
        if self.request.method == 'GET':
            if self.request.GET.get('page'):
                self.request.session['page'] = self.request.GET.get('page')
        return context

def add_product(request):
    if request.method == 'POST':
        if 'img' in request.FILES:
            new_product = Product.objects.create(
                name=request.POST['name'],
                description=request.POST['description'],
                price=request.POST['price'],
                stock=request.POST['stock'],
                main_image=request.FILES['img']
            )
        else:
            new_product = Product.objects.create(
                name=request.POST['name'],
                description=request.POST['description'],
                price=request.POST['price'],
                stock=request.POST['stock'],
            )
        if request.POST['new_category'] != '':
            new_category = Category.objects.create(name=request.POST['new_category'])
            new_product.categories.add(new_category)
        else:
            category =Category.objects.get(id=int(request.POST['category']))
            new_product.categories.add(category)
        new_product.save()
        if 'page' in request.session:    
            page = request.session['page']
            return redirect(f'/dashboard/products?page={page}')
        else:
            return redirect('dashboard_products')

def update_product(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        product = Product.objects.get(id=pk)
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        if request.POST['new_category'] != '':
            new_category = Category.objects.create(name=request.POST['new_category'])
            product.categories.add(new_category)
        else:
            category =Category.objects.get(id=int(request.POST['category']))
            product.categories.add(category)
        product.save()
        if 'img' in request.FILES:
            new_subimage = ProductImage.objects.create(product=product, image=request.FILES['img'])
        if request.POST['make_main'] != product.main_image:
            if product.main_image != '':
                move_to_subimage = ProductImage.objects.create(product=product, image=product.main_image)
                product.main_image.delete()
            product.main_image = request.POST['make_main']
            moved_to_mainimage = ProductImage.objects.get(image=request.POST['make_main'])
            moved_to_mainimage.delete()
            product.save()
    if 'page' in request.session:    
        page = request.session['page']
        return redirect(f'/dashboard/products?page={page}')
    else:
        return redirect('dashboard_products')

def delete_product(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(id=pk)
        product.delete()
    if 'page' in request.session:    
        page = request.session['page']
        return redirect(f'/dashboard/products?page={page}')
    else:
        return redirect('dashboard_products')

def delete_image(request, pk, place):
    if request.method == 'GET':
        if place == 'main':
            product = Product.objects.get(id=pk)
            product.main_image.delete()
        else:
            sub_image = ProductImage.objects.get(id=pk)
            sub_image.delete()
    if 'page' in request.session:    
        page = request.session['page']
        return redirect(f'/dashboard/products?page={page}')
    else:
        return redirect('dashboard_products')

def remove_category(request, product_pk, category_pk):
    if request.method == 'GET':
        product = Product.objects.get(id=product_pk)
        category = Category.objects.get(id=category_pk)
        product.categories.remove(category)
    if 'page' in request.session:    
        page = request.session['page']
        return redirect(f'/dashboard/products?page={page}')
    else:
        return redirect('dashboard_products')