from django.db import models
from socialuser.models import User

# Create your models here.


class Idea(models.Model):
    # Constants in Model class
    PUBLIC = "PUB"
    PROTECTED = "PRO"
    PRIVATE = "PRV"

    SHARE_IDEA_CHOICES = (
        (PUBLIC, "Public"),
        (PROTECTED, "Protected"),
        (PRIVATE, "Private"),
    )

    content = models.CharField(max_length=255, blank=False, null=False)
    privacity = models.CharField(
        max_length=3, choices=SHARE_IDEA_CHOICES, default=PUBLIC,
    )
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="ideauser", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content}. By: {self.user.username}. Privacy: {self.privacity}"
