from django.contrib import admin
from .models import Category, Account, Location, Person, Item, Movement, Supplier

admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Location)
admin.site.register(Person)
admin.site.register(Item)
admin.site.register(Movement)
admin.site.register(Supplier)