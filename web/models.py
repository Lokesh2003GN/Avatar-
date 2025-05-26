from django.db import models
from django.db.models import Max

class Catagory(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    Catagory_image_url = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(max_length=10000000, null=False, blank=False)
    color = models.CharField(max_length=150, null=False, blank=False, default='#8ecae6')

    def __str__(self):
        return self.name


class Character(models.Model):
    #catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, default=False)
    catagory = models.ManyToManyField(Catagory, related_name="characters")
    name = models.CharField(max_length=150, null=False, blank=False)
    Character_image_url = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(max_length=10000000, null=False, blank=False)
    priority = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.priority is None:
            # Set the priority value to the next highest value in the Character table
            max_priority = Character.objects.aggregate(Max('priority'))['priority__max']
            self.priority = (max_priority or 0) + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Get the priority of the character being deleted
        deleted_character_priority = self.priority
        
        # Call the superclass delete method
        super().delete(*args, **kwargs)
        
        # After deletion, adjust the priority of all characters with higher priority
        characters_to_update = Character.objects.filter(priority__gt=deleted_character_priority)
        for character in characters_to_update:
            character.priority -= 1
            character.save()

    def __str__(self):
        return self.name


class Character_Details(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, default=False)
    number = models.IntegerField(null=False, blank=False)
    title = models.CharField(max_length=150, null=True, blank=True)
    body = models.TextField(max_length=10000000, null=False, blank=False)
    hide_title = models.BooleanField(default=True, help_text="0-show, 1-hidden")

    @property
    def catagory(self):
        return self.character.catagory

    def __str__(self):
        return self.title if self.title else f"Character Detail {self.number}"