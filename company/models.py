from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class Product(models.Model):
    name = models.CharField(max_length = 80,verbose_name=" نام محصول")
    price = models.IntegerField(verbose_name=" قیمت هر کیلوگرم به تومان")
    quantity = models.DecimalField(max_digits=6, decimal_places=2,verbose_name=" مقدار به کیلوگرم")
    classification = models.ForeignKey("Classification", on_delete=models.CASCADE, verbose_name="دسته بندی")
    pic = models.ImageField(verbose_name="تصویر محصول")
   #؟
    supplier = models.ManyToManyField('Supplier', verbose_name="تامین کننده")

    grade = models.CharField(max_length = 20,verbose_name="کیفیت", choices= [('a','درجه یک'),('b','درجه دو')], default= ('a','درجه یک'))

    def __str__(self):
        return self.name

class Classification(models.Model):
    title = models.CharField(max_length = 100, verbose_name="دسته بندی")
    
    def __str__(self):
        return self.title
    
class City(models.Model):
    name = models.CharField(max_length = 100, verbose_name="نام شهر")
        
    def __str__(self):
        return self.name
        
class Inventory(models.Model):
    city = models.ForeignKey("City", on_delete = models.CASCADE, verbose_name="شهر انبار")
        
    def __str__(self):
        return str(self.city)

class InventoryProduct(models.Model):
    name = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name=" نام محصول")
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE, verbose_name="انبار")
    quantity = models.PositiveIntegerField(blank=False, verbose_name="مقدار به کیلوگرم")

    def __str__(self):
        return self.name.name

#؟
class Supplier(models.Model):
    name = models.CharField(max_length=80, verbose_name="نام تامین کننده")
    email = models.EmailField(verbose_name="ایمیل")
    phone_regex  = RegexValidator(regex=r'^\+?98?\d{9,15}$', message="Phone number must be entered in the format: '+989123456789'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True , default="+989123456789",verbose_name="تلفن همراه")
    
    def __str__(self):
        return self.name


class ShoppingBasket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
        
    def __str__(self):
        return self.name

class BasketItem(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE, verbose_name="محصول")
    shopping_basket = models.ForeignKey('ShoppingBasket', on_delete = models.CASCADE, verbose_name="سبد خرید")

        
    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name="سفارش", default= '')

    def __str__(self):
        return self.user

class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE, verbose_name="نام محصول")
    order = models.ForeignKey('Order', on_delete = models.CASCADE, verbose_name="سفارش")
        
    def __str__(self):
        return self.product
