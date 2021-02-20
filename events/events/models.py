from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime

class Event(models.Model):
    
    class StateChoices(models.TextChoices):
        DRAFT = 'DF',_('Draft')
        PUBLIC = 'PU',_('Public')
        PRIVATE = 'PR',_('Private')
    
    title = models.CharField(_("Title"),max_length=30,unique=True,blank=False,default='')
    description = models.TextField(_("Description"),max_length=200,null=False,default='')
    dateCreated = models.DateField(_("Date"),default=datetime.date.today)
    author = models.CharField(_("Author"),max_length=20,blank=True,default='')
    state = models.CharField(_("State"),max_length=2,
            choices=StateChoices.choices,
            default=StateChoices.DRAFT)

    class Meta:
        ordering = ['dateCreated']

    def __str__(self):
        return self.id +" "+self.title + " " +self.date
