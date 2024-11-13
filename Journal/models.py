from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

# Create your models here.
class SubscribedUsers(models.Model):
    email = models.EmailField(unique=True,max_length = 100)
    created_date = models.DateTimeField('Date created',default=timezone.now)


    def __str__(self):
        return self.email
    
class Events(models.Model):
    # Required Fields
    name = models.CharField(max_length=100, help_text="A unique identifier for the event, such as a short name or code.")
    title = models.CharField(max_length=200, help_text="Full title of the event.")
    description = models.TextField(help_text="Detailed description of the event.")
    image = models.ImageField(upload_to='uploads/event/', null=True, blank=True, help_text="An image representing the event.")
    date = models.DateTimeField(help_text="Date and time when the event is scheduled to take place.")
    location = models.CharField(max_length=255, help_text="Venue or location where the event will take place.")
    organizer = models.CharField(max_length=100, help_text="The person or organization hosting the event.")
    contact_email = models.EmailField(null=True, blank=True, help_text="Contact email for event inquiries.")
    is_virtual = models.BooleanField(default=False, help_text="Indicates if the event is virtual or in-person.")
    registration_link = models.URLField(null=True, blank=True, help_text="Link for participants to register for the event.")


    def __str__(self):
        return self.title   
    

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["-date"]  # Orders events by date in descending order
    
