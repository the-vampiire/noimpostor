from django.db.models import Model, IntegerField, OneToOneField, ForeignKey, CASCADE
from django.contrib.auth.models import User
from root.base_model import Base
from enum import Enum

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


class DefaultPrivacy(Model):
    class Meta:
        db_table = 'default_privacy'

    user = OneToOneField(to = User, on_delete = CASCADE)
    setting = IntegerField(
        choices = Privacy.as_choices(),
        default = Privacy.private,
        verbose_name = 'Default Privacy Setting'
    )

class Follow(Base):
    class Meta:
        db_table = 'follows'
        unique_together = ('following', 'follower')

    # user.followers.all()[.filter()] -> returns a users followers
    following = ForeignKey(User, on_delete = CASCADE, related_name = 'followers')
    
    # user.following.all()[.filter()] -> returns users followed by the user
    follower = ForeignKey(User, on_delete = CASCADE, related_name = 'following')