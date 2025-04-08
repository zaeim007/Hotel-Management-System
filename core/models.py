from django.db import models
from django.utils import timezone

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    is_occupied = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Room {self.room_number}"
    
    def check_in(self):
        self.is_occupied = True
        self.check_in_time = timezone.now()
        self.check_out_time = None
        self.save()
        
    def check_out(self):
        self.is_occupied = False
        self.check_out_time = timezone.now()
        self.save()

class Guest(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    num_guests = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='guests')
    check_in_date = models.DateTimeField(auto_now_add=True)
    check_out_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def check_out(self):
        if self.room:
            self.room.check_out()
            self.check_out_date = timezone.now()
            self.save()
