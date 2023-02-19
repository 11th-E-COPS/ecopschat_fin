from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from chat.forms import RoomForm
from chat.models import Room

# Create your views here.
def index(request):
    return render(request, "chat/index.html")


def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room: Room = form.save()
            return redirect("chat:room_chat", created_room.pk)
    else:
        form = RoomForm()

    return render(request, "chat/room_form.html",{
        "form":form,
    })
def room_chat(request, room_pk):
    room=get_object_or_404(Room,pk=room_pk)
    return render(request,"chat/room_chat.html",{
        "room":room,
    })
