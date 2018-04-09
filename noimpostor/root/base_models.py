from django.db.models import (
    Model,
    DateTimeField,
    CharField,
    TextField,
    IntegerField,
    ForeignKey,
    CASCADE
)
from django.contrib.auth.models import User
from datetime import datetime
from enum import Enum

class Base(Model):
    """
    Base model from which all project models will inherit

    inherits Django Model class and provides 'created' and 'updated' fields
    overrides the save() method to inject values automatically on save
    """
    class Meta:
        abstract = True

    created = DateTimeField(editable = False)
    updated = DateTimeField(editable = False)

    # overload the save() method to apply automatic values on creation / updating
    def save(self, *args, **kwargs):
        if not self.pk: # if the object is new it will not have a primary key prop
            self.created = datetime.now() # give it a creation timestamp
        self.updated = datetime.now() # in both scenarios give it an update timestamp

        # call parent (models.Model) save() method
        return super(Base, self).save(*args, **kwargs) 

class Privacy(Enum):
    """
    Privacy settings to be used in the Post and User models as enums

    -1, private: exclusive to the user
     0, anonymous: in public feed but with no association to user
     1, public: in public feed with a link to the user profile
    """
    private = -1
    anonymous = 0
    public = 1

    @classmethod
    def as_choices(cls):
        return [(option.value, option.name) for option in cls]

class Post(Base):
    class Meta:
        abstract = True

    title = CharField(blank = False, max_length = 140)
    notes = TextField(blank = True)
    user = ForeignKey(User, on_delete = CASCADE, related_name = 'challenges')
    privacy = IntegerField(
        choices = Privacy.as_choices(),
        default = Privacy.private,
        verbose_name = 'Privacy Setting'
    )


