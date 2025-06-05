from django.urls import path
from .views import *

urlpatterns = [
    path('create-event/', CreateEventView.as_view()),
    path('upcoming-events/', UpcomingEventsView.as_view()),
    path('events/<int:event_id>/register/', RegisterAttendeeView.as_view()),
    path('events/<int:event_id>/attendees/', EventAttendeesView.as_view()),
]
