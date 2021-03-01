from django import forms
from .models import Event, Subscription
from django.forms import NumberInput
from django.utils.translation import gettext_lazy as _

class EventForm(forms.ModelForm):

    '''
        Form class tied to Event Model
    '''

    ## custom form fields
    date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    state = forms.ChoiceField(choices=Event.StateChoices.choices)

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        ## field placeholders
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'placeholder': _('title')})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['description'].widget.attrs.update(
            {'placeholder': _('description')}
        )
        if kwargs['instance'] != None: ## inserts previous data on event update
            self.fields['title'].widget.attrs.update({'placeholder': _('title')})
            self.fields['title'].widget.attrs.update({'placeholder': _('description')})
            self.fields['title'].widget.attrs.update({'placeholder': _('date')})
            self.fields['title'].widget.attrs.update({'placeholder': _('state')})


    class Meta:
        model = Event
        exclude = ['author'] ## all fields except author are required


class SubscriptionForm(forms.ModelForm):

    username = forms.CharField(label='username', max_length=60)
    email = forms.CharField(label='email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ## placceholders on subscription form
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update(
            {'placeholder': _('username')}
        )
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': _('email')})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update(
            {'placeholder': _('comment')}
        )

    class Meta:
        model = Subscription
        exclude = ['event', 'date'] ## excluding as editable fields
        fields = ('comment', ) 
        ## if user is authenticated this field in fields
        ## is locked and filled with authenticated user username
        ## and email
        ## if user is anonymous, only the fronted is correctly stopping
        ## the data from being submitted
        ## possible server error if form is submitted with those fields
        ## blanked
