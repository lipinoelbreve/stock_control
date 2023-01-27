from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import date

STATUS = [
    ('available','Available'),
    ('in_use','In Use'),
    ('repair','Repair'),
    ('disposed', 'Disposed')
]



class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    #prefix = models.CharField(max_length=4, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    part_number = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='accounts')
    description = models.TextField(blank=True, null=True)

    available_qty = models.IntegerField(default=0)
    in_use_qty = models.IntegerField(default=0)
    repair_qty = models.IntegerField(default=0)
    disposed_qty = models.IntegerField(default=0)
    total_qty = models.IntegerField(default=0)

    @property
    def count_items(self):
        available_qty = self.items.filter(status = 'available').count()
        in_use_qty = self.items.filter(status = 'in_use').count()
        repair_qty = self.items.filter(status = 'repair').count()
        disposed_qty = self.items.filter(status = 'disposed').count()
        self.total_qty = available_qty + in_use_qty + repair_qty

        self.available_qty = available_qty
        self.in_use_qty = in_use_qty
        self.repair_qty = repair_qty
        self.disposed_qty = disposed_qty

        self.save()

    def __str__(self):
        return self.name

class Location(MPTTModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    item_count = models.IntegerField(default=0)

    @property
    def count_items(self):
        count = self.items.exclude(status='disposed').count()
        self.item_count = count
        self.save()

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    item_count = models.IntegerField(default=0)

    @property
    def count_items(self):
        count = self.items.exclude(status='disposed').count()
        self.item_count = count
        self.save()

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    serial_number = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='items', blank=False, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='items', blank=False, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='items', blank=True, null=True)
    user = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='items', blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, blank=True, null=True)
    trello = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, related_name='items', blank=True, null=True)
    last_movement = models.ForeignKey('Movement', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    date_created = models.DateField(default=date.today)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Movement(models.Model):
    MOVEMENT_TYPES = [
        ('creation','Creation'),
        ('transfer','Transfer'),
        ('repair','Repair'),
        ('dispose', 'Dispose')
    ]
        
    movement_type = models.CharField(max_length=100, choices=MOVEMENT_TYPES, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='movements')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='movements')
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='movements')
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.movement_type.title() + ' ' + str(self.item) + ' >> ' + str(self.location) + ' - ' + str(self.user)