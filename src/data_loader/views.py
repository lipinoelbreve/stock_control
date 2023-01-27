from django.shortcuts import render, redirect
from django.conf import settings
from .models import *
from .forms import *
import base64
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.contrib.auth.decorators import login_required

#%% ACCOUNTS

@login_required
def accounts(request):
    title = 'Accounts'
    accounts = Account.objects.order_by('id')
    
    context = {
        'title': title,
        'accounts': accounts
    }
    return render(request, 'data_loader/accounts.html', context)

@login_required
def view_account(request, id):
    account = Account.objects.get(pk = id)
    attrs = [(field.name.title(), getattr(account, field.name)) for field in account._meta.fields]

    items = account.items.all().order_by('pk')

    context = {
        'title': account.name,
        'attrs': attrs,
        'items': items
    }

    return render(request, 'data_loader/view_account.html', context)    

#%% ITEMS

@login_required
def items(request):
    title = 'Items'
    items = Item.objects.order_by('id')
    context = {
        'title': title,
        'items': items
    }
    return render(request, 'data_loader/items.html', context)

@login_required
def add_item(request):
    form = AddItem(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.serial_number = instance.account.part_number + str(len(Item.objects.filter(account = instance.account)) + 1).zfill(6)
        instance.save()

        request.method ='GET'
        return redirect('data_loader:add_movement', item_id=instance.pk)

    form = AddItem()
    context = {
        'form': form,
        'title': 'Add Item'
    }
    return render(request, 'data_loader/add_item.html', context)

@login_required
def edit_item(request, id):
    item = Item.objects.get(pk=id)
    form = AddItem(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('data_loader:items')
    else:
        context = {
            'form': form,
            'title': 'Edit Item'
        }
        return render(request, 'data_loader/add_item.html', context)

@login_required
def view_item(request, id):
    item = Item.objects.get(pk = id)
    attrs = [(field.name.title(), getattr(item, field.name)) for field in item._meta.fields]

    movements = item.movements.all().order_by('pk')

    context = {
        'title': item.name,
        'item_id': id,
        'attrs': attrs,
        'movements': movements
    }

    return render(request, 'data_loader/view_item.html', context)

@login_required
def view_qr(request, id):
    item = Item.objects.get(pk=id)
    data = request.get_host() + '/data_loader/view_item/' + str(id)
    img = qrcode.make(data)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_data = base64.b64encode(img_io.read()).decode()
    context = {
        'h1': item.serial_number,
        'h2': 'Epic Aerospace',
        'img': img_data
    }

    return render(request, 'data_loader/view_qr.html', context=context)

#%% MOVEMENTS

@login_required
def movements(request):
    title = 'Movements'
    movements_values = Movement.objects.order_by('id')
    context = {
        'title': title,
        'movements': movements_values
    }
    return render(request, 'data_loader/movements.html', context)

@login_required
def add_movement(request, item_id):
    item = Item.objects.get(pk = item_id)
    last_movement = item.last_movement
    
    if last_movement is None:
        form = AddMovement(request.POST or None, initial={'movement_type':'creation', 'date': date.today()}, new=True)
        form.fields['movement_type'].widget = forms.HiddenInput()
    else:
        form = AddMovement(request.POST or None, initial={'movement_type':'transfer', 'date': date.today()}, new=False)

    if form.is_valid():
        instance = form.save(commit=False)
    
        instance.item = item
        instance.save()

        item.location = instance.location
        item.user = instance.user

        # Me fijo a donde va a estar
        item.status = 'in_use'
        if instance.user.name == 'All':
            item.status = 'available'
        if instance.movement_type == 'repair':
            item.status = 'repair'
        elif instance.movement_type == 'dispose':
            item.status = 'disposed'

        item.last_movement = instance
        item.save()

        # Actualizo lo viejo:
        if last_movement is not None:
            last_movement.location.count_items
            last_movement.user.count_items

        # Actualizo lo nuevo:
        item.account.count_items
        item.location.count_items
        item.user.count_items

        return redirect('data_loader:items')
    context = {
        'form': form,
        'title': 'Add Movement'
    }
    return render(request, 'data_loader/add_movement.html', context)

@login_required
def view_movement(request, id):
    movement = Movement.objects.get(pk = id)
    attrs = [(field.name.title(), getattr(movement, field.name)) for field in movement._meta.fields]

    #movements = movement.movements.all().order_by('pk')

    context = {
        'title': movement,
        'movement_id': id,
        'attrs': attrs,
        #'movements': movements
    }

    return render(request, 'data_loader/view_movement.html', context)

#%% LOCATIONS

@login_required
def locations(request):
    title = 'Locations'
    locations = Location.objects.order_by('id')
    
    context = {
        'title': title,
        'locations': locations
    }
    return render(request, 'data_loader/locations.html', context)

#%% PEOPLE

@login_required
def people(request):
    title = 'People'
    people = Person.objects.order_by('id')
    
    context = {
        'title': title,
        'people': people
    }
    return render(request, 'data_loader/people.html', context)

#%% AJAX

@login_required
def load_accounts(request):
    cat_id = request.GET.get('category')
    if cat_id == '':
        accounts = Account.objects.none()
    else:
        accounts = Account.objects.filter(category = cat_id).all() # podría usar mejor el related_name
    return render(request, 'data_loader/account_dropdown.html', {'accounts': accounts})