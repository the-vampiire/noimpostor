from django.contrib.auth.models import User
from django.db.models import IntegerField, ForeignKey, CASCADE
from root.base_models import Base, Post

"""
TODO

Accomplishments and Challenges are extremely similar
variations are only in the x_level field

Similarly Empathy and Inspiration are both similar
variation only in the Post-like fk [accomplishment, challenge]

Can all of these be placed into a polymorphic Post and Reaction table?
Pros and Cons?
How does Django / its ORM process polymorphic relationships?
"""


class Accomplishment(Post):
    """
    inherits title, notes, and privacy from Post
    inherits created and updated from Base (Post parent inheritance)
    """
    class Meta:
        db_table = 'accomplishments'

    user = ForeignKey(User, on_delete = CASCADE, related_name = 'accomplishments')

    _accomplishment_levels = (
        (index, value) for index, value in enumerate(
            [
                "Stepping stone",
                "Milestone",
                "Eventful",
                "Life changing",
                "I am become Wizard"
            ]
        )
    )
    accomplishment_level = IntegerField(choices = _accomplishment_levels, default = 0, verbose_name = 'Accomplishment Level')

class Inspiration(Base):
    """
    Tracks an authed users Inspiration on another users Accomplishment

    For when a user views a public / Anonymous Accomplishment and is inspired by it

    Users can mark accomplishments that inspire them

    Accomplishment authors can see the users they have inspired 
    """
    class Meta:
        db_table = 'inspiration'
        unique_together = ('inspired_user', 'accomplishment')

    # user.inspiring_accomplishments.all()[.filter()] -> users accomplishments that others have been inspired by
    inspired_user = ForeignKey(User, on_delete = CASCADE, related_name = 'inspirations')
    # accomplishment.inspired_users.all()[.filter()] -> all of the users who have been inspired by the accomplishment
    accomplishment = ForeignKey(Accomplishment, on_delete = CASCADE, related_name = 'inspired_users')
