from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    name = models.CharField(max_length=500)
    email = models.EmailField()

    class Meta:
        unique_together = ('event', 'email')  # Prevent duplicate registration

    def __str__(self):
        return self.event

