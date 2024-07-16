from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



class User(AbstractUser):
    is_farmer = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farmer_id = models.AutoField(primary_key=True)
    farmerUsername = models.CharField(max_length=100)
    farmerPhone = models.CharField(max_length=15, blank=True, null=True)
    farmerEmail = models.EmailField(max_length=100, blank=True, null=True)
    farmerAddress = models.CharField(max_length=100, blank=True, null=True)

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    consumer_id = models.AutoField(primary_key=True)
    consumerUsername= models.CharField(max_length=100)
    consumerPhone= models.CharField(max_length=15)
    consumerAddress=models.CharField(max_length=100,  blank=True, null=True) 
    consumerEmail = models.EmailField(max_length=100,  blank=True, null=True)


class Farm(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    numberOfhens = models.PositiveIntegerField()
    
    
    @property
    def total_stock(self):
        return self.egg_inventories.aggregate(total=models.Sum('stock'))['total'] or 0

    def __str__(self):
        return self.name 
    
class eggInventory(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='egg_inventories')
    stock = models.IntegerField()
    trayPrice = models.IntegerField()
    posted_on = models.DateTimeField(auto_now_add=True)
    batch_number = models.CharField(max_length=100, default='default_batch')

    def __str__(self):
        return f'{self.batch_number} - {self.farm.name}'


class EggBatch(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='egg_batches')
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.farm.name} - {self.quantity}'

class expenseInventory(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='expense_inventories')
    particulars = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unitPrice = models.IntegerField()


    @property
    def total_cost(self):
        return self.quantity * self.unitPrice

    def __str__(self):
        return f"{self.farm.name} - {self.particulars}"
    



class Order(models.Model):
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.consumer.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    egg_batch = models.ForeignKey(eggInventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} from {self.egg_batch.batch_number}'