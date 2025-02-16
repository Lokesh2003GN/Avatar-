from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Character
from django.db.models import F
from django.db.models import Max  # Import Max here


#characters = Character.objects.all()
#temp=1
#for index, character in enumerate(characters, start=1):
#            character.priority = temp
#            character.save()
#            temp+=1



@receiver(pre_save, sender=Character)
def adjust_priority(sender, instance, **kwargs):
    if instance.pk:  # Ensure this is not a new instance
        try:
            original = Character.objects.get(pk=instance.pk)
            if original.priority != instance.priority:  # Check if priority has changed
                # Shift priorities between the old and new values
                if original.priority < instance.priority:
                    # Decrease priorities in the range
                    Character.objects.filter(
                        priority__gt=original.priority, priority__lte=instance.priority
                    ).update(priority=F('priority') - 1)
                else:
                    # Increase priorities in the range
                    Character.objects.filter(
                        priority__gte=instance.priority, priority__lt=original.priority
                    ).update(priority=F('priority') + 1)
        except Character.DoesNotExist:
            pass  # This won't happen for an existing object
    else:
        # Handle new instance priority collision
        if Character.objects.filter(priority=instance.priority).exists():
            Character.objects.filter(priority__gte=instance.priority).update(
                priority=F('priority') + 1
            )