from django import forms

from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'
    size=1

class AddItem(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['serial_number', 'last_modified', 'location', 'user', 'last_movement', 'status']
        widgets = {
            'date_created':DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.none()

        if 'category' in self.data:
            try:
                cat_id = int(self.data.get('category'))
                accounts = Account.objects.filter(category = cat_id)

                self.fields['account'].queryset = accounts

            except:
                pass
        elif self.instance.pk:
            self.fields['account'].queryset = self.instance.category.accounts.order_by('name')


class AddMovement(forms.ModelForm):
    class Meta:
        model = Movement
        fields = '__all__'
        exclude = ['item']
        widgets = {
            'date':DateInput()
        }


    def __init__(self, *args, **kwargs):
        #self.item = kwargs.pop('item', None)
        self.new = kwargs.pop('new', None)
        super().__init__(*args, **kwargs)
        if self.new == False:
            self.fields['movement_type'].choices = [choice for choice in Movement.MOVEMENT_TYPES if choice[0] != 'creation']