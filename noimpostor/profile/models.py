from django.db.models import Model, IntegerField, OneToOneField, ForeignKey, CASCADE
from django.contrib.auth.models import User
from root.base_models import Base, Privacy

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