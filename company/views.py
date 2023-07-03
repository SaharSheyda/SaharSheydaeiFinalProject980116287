from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutUsView(TemplateView):
    template_name = 'about-us.html'

class ContactUsView(TemplateView):
    template_name = 'contact-us.html'

class JobsView(TemplateView):
    template_name = 'jobs.html'

class ShopView(TemplateView):
    template_name = 'shop.html'

#admin views

#product
class ProductView(ListView):
    model = Product
    template_name = 'product.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product-create.html'
    fields = '__all__'
    success_url = reverse_lazy('product.html')

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product-detail.html'
    fields = '__all__'

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product-update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('product-detail', args=(self.object.id,))

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product-delete.html'
    success_url = reverse_lazy('product')

#classification
class ClassificationListView(ListView):
    model = Classification
    template_name = 'classification.html'


class ClassificationCreateView(LoginRequiredMixin, CreateView):
    model = Classification
    template_name = 'classification-create.html' 
    fields = "__all__"
    success_url = reverse_lazy('classification')


class ClassificationDeleteView(LoginRequiredMixin, DeleteView): 
    model = Classification
    template_name = 'classification-delete.html' 
    success_url = reverse_lazy('classification')

#City
class CityListView(LoginRequiredMixin, ListView):
    model = City
    template_name = 'city.html'


class CityCreateView(LoginRequiredMixin, CreateView):
    model = City
    template_name = 'city-create.html' 
    fields = "__all__"
    success_url = reverse_lazy('city')


class CityDeleteView(LoginRequiredMixin, DeleteView): 
    model = City 
    template_name = 'city-delete.html' 
    success_url = reverse_lazy('city')

#Inventory

class InventoryListView(LoginRequiredMixin, ListView):
    model = Inventory
    template_name = 'inventory.html'


class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = Inventory
    template_name = 'inventory-create.html' 
    fields = "__all__"
    success_url = reverse_lazy('inventory')


class InventoryDeleteView(LoginRequiredMixin, DeleteView): 
    model = Inventory 
    template_name = 'inventory-delete.html' 
    success_url = reverse_lazy('inventory')

#InventoryProduct

class InventoryProductListView(LoginRequiredMixin, ListView):
    model = InventoryProduct
    template_name = 'inventoryProduct.html'


class InventoryProductCreateView(LoginRequiredMixin, CreateView):
    model = InventoryProduct
    template_name = 'inventoryProduct_new.html' 
    fields = "__all__"
    success_url = reverse_lazy('inventoryProduct')


class InventoryProductDeleteView(LoginRequiredMixin, DeleteView): 
    model = InventoryProduct 
    template_name = 'inventoryProduct_delete.html' 
    success_url = reverse_lazy('inventoryProduct')

#Order

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order.html'


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'order-update.html' 
    fields = "__all__"
    success_url = reverse_lazy('order')


class OrderDeleteView(LoginRequiredMixin, DeleteView): 
    model = Order 
    template_name = 'order-delete.html' 
    success_url = reverse_lazy('order')


#---------------------------------------------------------

#users purchaseable products based on their city
class UserProductListView(LoginRequiredMixin, ListView):
    model = InventoryProduct
    template_name= 'adminpannel.html'
    
    def get_queryset(self):
        return InventoryProduct.objects.filter(inventory__city=self.request.user.city)

#user order submit view    
@login_required(login_url='login')
def userOrderSubmitView(request, pk):
    if request.method == 'POST':
        product = InventoryProduct.objects.get(id=pk)
        quantity = request.POST.get('quantity')
        if product.quantity >= int(quantity):
            product.quantity -= int(quantity)
            product.save()
            newOrder = Order.objects.create(username=request.user, product=product, quantity=quantity)
            newOrder.save()
            return render(request, 'order-success.html')
        else:
            return render(request, 'order-error.html')
        
    else:
        product = InventoryProduct.objects.get(id=pk)
        context = {
                'productInventory': product,
            }
        return render(request, 'userOrder.html', context)


#users previous orders view
class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name= 'userOrderList.html'
    
    def get_queryset(self):
        return Order.objects.filter(username=self.request.user)