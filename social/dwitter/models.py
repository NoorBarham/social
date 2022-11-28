from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,#user do not need to re follow 
        blank=True,#the user can have empty follower
        )
    def __str__(self):
        return self.user.username
    
#signal to create profile for every user created 
@receiver(post_save, sender=User)# instead of post_save.connect
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])#to make the user follow himself
        user_profile.save()
      
class Dweet(models.Model):
    user = models.ForeignKey(User, related_name="dweets", on_delete=models.DO_NOTHING)#related_name:to access the dweets from the user
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.user} "
                f"({self.created_at:%Y-%m-%d %H:%M}): "
                f"{self.body[:30]}...")