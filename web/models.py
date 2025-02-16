from django.db import models
from django.db.models import Max
from django.core.exceptions import ValidationError

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


class Quize(models.Model):
    question = models.CharField(max_length=250, null=False, blank=False)
    op1 = models.CharField(max_length=250, null=False, blank=False)
    op1_img_url = models.CharField(max_length=250, null=True, blank=True)
    op2 = models.CharField(max_length=250, null=False, blank=False)
    op2_img_url = models.CharField(max_length=250, null=True, blank=True)
    op3 = models.CharField(max_length=250, null=True, blank=True)
    op3_img_url = models.CharField(max_length=250, null=True, blank=True)
    op4 = models.CharField(max_length=250, null=True, blank=True)
    op4_img_url = models.CharField(max_length=250, null=True, blank=True)
    ANSWER_CHOICES=[
    ('op1','option 1'),
    ('op2','option 2'),
    ('op3','option 3'),
    ('op4','option 4'),
    ]
    ans = models.CharField(max_length=3, choices=ANSWER_CHOICES,null=False, blank=False) 

    DEFACULTY_CHOICES = [
        ('1', 'Easy'),
        ('2', 'Medium'),
        ('3', 'Hard'),
    ]
    defaculty = models.CharField(max_length=1, choices=DEFACULTY_CHOICES, null=False, blank=False)

    def __str__(self):
        return self.question

    #def clean(self):
#        # Ensure ans matches one of the options
#        valid_answers = [self.op1, self.op2, self.op3, self.op4]
#        if self.ans not in valid_answers:
#            raise ValidationError("The correct answer must match one of the options.")

    def get_answer_choices(self):
        # Generate choices for admin dropdown dynamically
        return [('op1',self.op1), ('op2',self.op2), ('op3',self.op3), ( 'op4',self.op4)]

#class Quize(models.Model):
#    question = models.CharField(max_length=250, null=False, blank=False)
#    op1 = models.CharField(max_length=250, null=False, blank=False)
#    op1_img_url = models.CharField(max_length=250, null=True, blank=True)
#    op2 = models.CharField(max_length=250, null=False, blank=False)
#    op2_img_url = models.CharField(max_length=250, null=True, blank=True)
#    op3 = models.CharField(max_length=250, null=True, blank=True)
#    op3_img_url = models.CharField(max_length=250, null=True, blank=True)
#    op4 = models.CharField(max_length=250, null=True, blank=True)
#    op4_img_url = models.CharField(max_length=250, null=True, blank=True)
#    
#    # The answer field that stores the correct answer as a choice
#    ANSWER_CHOICES = [
#        (op1, 'Option 1'),
#        (op2, 'Option 2'),
#        (op3, 'Option 3'),
#        (op4, 'Option 4'),
#    ]
#    ans = models.CharField(max_length=3, choices=ANSWER_CHOICES, null=False, blank=False)
    
#DEFACULTY_CHOICES = [
#        ('1', 'Easy'),
#        ('2', 'Medium'),
#        ('3', 'Hard'),
#    ]
#    defaculty=models.CharField(max_length=1, choices=DEFACULTY_CHOICES, null=False, blank=False)
#    def __str__(self):
#        return self.question

	
	
	
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