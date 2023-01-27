""" DATA LOADER URLs """

from django.urls import path
from . import views

app_name = 'data_loader'

urlpatterns = [
    path('accounts/', views.accounts, name='accounts'),
    path('view_account/<int:id>', views.view_account, name='view_account'),
    path('items/', views.items, name='items'),
    path('add_item/', views.add_item, name='add_item'),
    path('edit_item/<int:id>', views.edit_item, name='edit_item'),
    path('view_item/<int:id>', views.view_item, name='view_item'),
    path('view_qr/<int:id>', views.view_qr, name='view_qr'),
    path('movements/', views.movements, name='movements'),
    path('add_movement/<int:item_id>', views.add_movement, name='add_movement'),
    path('view_movement/<int:id>', views.view_movement, name='view_movement'),
    path('locations/', views.locations, name='locations'),
    path('people/', views.people, name='people'),
    path('ajax/load-accounts/', views.load_accounts, name='ajax_load_accounts'), # AJAX
]
