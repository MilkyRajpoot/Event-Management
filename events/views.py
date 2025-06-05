#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Attendee
from .serializers import EventSerializer
from django.utils import timezone

class CreateEventView(APIView):
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpcomingEventsView(APIView):
    def get(self, request):
        current_time = timezone.now()
        upcoming_events = Event.objects.filter(start_time__gt=current_time).order_by('start_time')
        serializer = EventSerializer(upcoming_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterAttendeeView(APIView):
    def post(self, request, event_id):
        email = request.data.get('email')
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        if event.attendees.count() >= event.max_capacity:
            return Response({"error": "Event is Full"}, status=status.HTTP_400_BAD_REQUEST)

        if event.attendees.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttendeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventAttendeesView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        attendees = event.attendees.all()
        serializer = AttendeeSerializer(attendees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)