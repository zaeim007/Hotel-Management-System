from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Room, Guest
from .forms import GuestForm, SearchForm

def home(request):
    """View for homepage"""
    return render(request, 'home.html')

def login_view(request):
    """View for login page"""
    return render(request, 'login.html')

@login_required
def dashboard(request):
    """Manager dashboard view"""
    # Count rooms and occupancy
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(is_occupied=True).count()
    available_rooms = total_rooms - occupied_rooms
    
    # Get recent check-ins
    recent_guests = Guest.objects.filter(check_out_date__isnull=True).order_by('-check_in_date')[:5]
    
    context = {
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': available_rooms,
        'occupancy_percentage': (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0,
        'recent_guests': recent_guests,
    }
    return render(request, 'dashboard.html', context)

@login_required
def room_status(request):
    """View all rooms and their status"""
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'room_status.html', {'rooms': rooms})


@login_required
def guest_list(request):
    """List all guests with search functionality"""
    search_form = SearchForm(request.GET or None)
    guests = Guest.objects.all().order_by('-check_in_date')
    
    if search_form.is_valid() and search_form.cleaned_data['query']:
        query = search_form.cleaned_data['query']
        guests = guests.filter(
            Q(name__icontains=query) | 
            Q(phone__icontains=query) | 
            Q(email__icontains=query)
        )
    
    return render(request, 'guest_list.html', {
        'guests': guests,
        'search_form': search_form
    })

@login_required
def check_in_guest(request):
    """Check in a new guest"""
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            room = form.cleaned_data['room']
            
            # Check if room is available
            if room.is_occupied:
                messages.error(request, f"Room {room.room_number} is already occupied.")
                return render(request, 'guest_form.html', {'form': form})
            
            # Process check-in
            room.check_in()
            guest.room = room
            guest.save()
            
            messages.success(request, f"Guest {guest.name} checked in to Room {room.room_number} successfully.")
            return redirect('room_status')
    else:
        form = GuestForm()
        # Only show available rooms in the form
        form.fields['room'].queryset = Room.objects.filter(is_occupied=False)
    
    return render(request, 'guest_form.html', {'form': form})

@login_required
def check_out_guest(request, guest_id):
    """Check out a guest"""
    guest = get_object_or_404(Guest, id=guest_id)
    
    if guest.check_out_date:
        messages.error(request, f"Guest {guest.name} has already checked out.")
    else:
        room = guest.room
        guest.check_out()
        messages.success(request, f"Guest {guest.name} checked out from Room {room.room_number} successfully.")
    
    return redirect('room_status')
