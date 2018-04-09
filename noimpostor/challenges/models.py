from django.contrib.auth.models import User
from django.db.models import IntegerField, ForeignKey, CASCADE
from root.base_models import Base, Post

class Challenge(Post):
    """
    inherits title, notes, and privacy from Post
    inherits created and updated from Base (Post parent inheritance)
    """
    class Meta:
        db_table = 'challenges'

    user = ForeignKey(User, on_delete = CASCADE, related_name = 'challenges')

    _impostor_levels = (
        (index, value) for index, value in enumerate(
            [
                "Shadow",
                "Looming",
                "Consumed",
                "Meltdown"
            ]
        )
    )
    impostor_level = IntegerField(choices = _impostor_levels, default = 0, verbose_name = 'Impostor Level')

class Empathy(Base):
    """
    Tracks an authed users Empathy on another users Challenge

    For when a user views a public / Anonymous challenge and empathizes with it
    
    Both users gain an understanding that they are not alone in their Challenge
    """
    class Meta:
        db_table = 'empathy'
        unique_together = ('empathizing_user', 'challenge')

    # empathizing_user.empathized_challenges.all() -> users challenges that empathize with
    empathizing_user = ForeignKey(User, on_delete = CASCADE, related_name = 'empathized_challenges')
    # challenge.empathizing_users.all() -> all of the users who have empathized with the challenge
    challenge = ForeignKey(Challenge, on_delete = CASCADE, related_name = 'empathizing_users')


    


    

    