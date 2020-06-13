from django.db import models
from django.db.models import F, Q
from socialuser.models import User

# Create your models here.


class UserRelation(models.Model):
    ACCEPTED = "ACC"
    PENDING = "PEN"
    DENIED = "DEN"

    FOLLOW_PETITION_CHOICES = (
        (ACCEPTED, "Acepted"),
        (PENDING, "Pending"),
        (DENIED, "Denied"),
    )

    user_follower = models.ForeignKey(
        User, related_name="userrelationfollower", on_delete=models.CASCADE
    )
    user_followed = models.ForeignKey(
        User, related_name="userrelationfollowed", on_delete=models.CASCADE
    )
    follow_status = models.CharField(
        max_length=3, choices=FOLLOW_PETITION_CHOICES, default=PENDING,
    )

    class Meta:
        unique_together = ("user_follower", "user_followed")
        constraints = [
            models.CheckConstraint(
                check=~Q(user_follower__exact=F("user_followed")), name="noautofollow"
            )
        ]

    def __str__(self):
        return (
            f"{self.user_follower.username} "
            f"follow {self.user_followed.username} "
            f"and status is {self.follow_status}"
        )
