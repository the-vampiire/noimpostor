from django.db.models import Model, DateTimeField
from datetime import datetime

class Base(Model):
    """
    Base model from which all project models will inherit

    inherits Django Model class and provides 'created' and 'updated' fields
    overrides the save() method to inject values automatically on save
    """
    class Meta:
        abstract = True

    created = DateTimeField(editable = False)
    updated = DateTimeField()

    # overload the save() method to apply automatic values on creation / updating
    def save(self, *args, **kwargs):
        if not self.pk: # if the object is new it will not have a primary key prop
            self.created = datetime.now() # give it a creation timestamp
        self.updated = datetime.now() # in both scenarios give it an update timestamp

        # call parent (models.Model) save() method
        return super(Base, self).save(*args, **kwargs) 
