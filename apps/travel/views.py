from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from .models import Destination
from ..login_registration.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    user = User.objects.get(id=request.session['id'])
    context = {
        "destinations": Destination.objects.filter(creator=user).distinct()|Destination.objects.filter(travelers=user).distinct().order_by('start_date'), #need to add many to many filter as well :)
        "not_destinations": Destination.objects.exclude(creator=user).exclude(travelers=user),
    }
    return render(request, 'travel/index.html', context)

def new(request):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    return render(request, 'travel/new.html')

def create(request):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        destinationObject = Destination.objects.isValidDestination(request.POST, user)
        if 'destination' in destinationObject:
            return redirect(reverse('travel:index'))
        else:
            for error in destinationObject['errors']:
                messages.warning(request, error)
            return redirect(reverse('travel:new'))
    else:
        return redirect(reverse('travel:index'))

def show(request, destination_id):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    context = {
        "destination": Destination.objects.get(id=destination_id),
    }
    return render(request, 'travel/show.html', context)
    
def join(request, destination_id):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    destination = Destination.objects.get(id=destination_id)
    user = User.objects.get(id=request.session['id'])

    destination.travelers.add(user)
    print "dest.trav.all()"
    print destination.travelers.all()
    return redirect(reverse('travel:index'))
    


'''
def delete_all(request):
    User.objects.all().delete()
    Destination.objects.all().delete()
    return redirect(reverse('auth:index'))
'''