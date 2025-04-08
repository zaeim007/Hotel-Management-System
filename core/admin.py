from django.contrib import admin
from .models import Room, Guest

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'is_occupied', 'check_in_time', 'check_out_time')
    search_fields = ('room_number',)
    list_filter = ('is_occupied',)

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'num_guests', 'room')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('check_in_date',)
