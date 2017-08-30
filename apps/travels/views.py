# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import models
import re
import bcrypt
import datetime

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

# Create your views here.

def main(request):
    if 'user_id' in request.session:
        request.session['user_id'] = None
        print request.session['user_id']
    return render(request, 'travels/main.html')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    request.session['name'] = result.name
    return redirect('/travels')

def register(request):
    if request.method == "POST":
        errors = []
        if len(request.POST['name']) < 3:
            errors.append("name must be at least 3 characters")
        if len(request.POST['username']) < 3:
            errors.append("username must be at least 3 characters")
        if len(request.POST['password']) < 8:
            errors.append("password must be at least 8 characters")
        if request.POST['password'] != request.POST['confirm_password']:
            errors.append("passwords do not match")
        if len(errors) > 0:
            print 'errors exist'
            for err in errors:
                messages.error(request, err)
            return redirect('/')
        else:
            print "no errors"
            hashed = bcrypt.hashpw((request.POST['password'].encode()), bcrypt.gensalt(5))
        
            new_user = User.objects.create(            
                name = request.POST['name'],
                username = request.POST['username'],
                password = hashed,
                )

            request.session['user_id'] = new_user.id
            request.session['name'] = new_user.name
            print request.session['user_id']
            print request.session['name']
    return redirect('/travels')

def travels(request):
    print request.session['user_id']
    print request.session['name']
    if 'user_id' not in request.session:
        return redirect(reverse("get_main"))
    context = {
        'top_list': User.objects.get(id=request.session['user_id']).travelers_trips.all(),
        'bottom_list': Trip.objects.exclude(trip_planner=request.session['user_id']),
    }
    print context['top_list'].values()
    # print context['top_list2'].values()
    print context['bottom_list']
    return render(request, 'travels/travels.html', context)

def create(request):
    if 'user_id' not in request.session:
        return redirect(reverse("get_main"))
    user_id = request.session['user_id']
    print user_id
    return render(request, 'travels/create.html')

def add_trip(request):
    print request.session['user_id']
    if request.method == "POST":
        errors = []
        if request.POST['new_destination'] == '':
            errors.append("Destination field cannot be empty!")
        if request.POST['new_description'] == '':
            errors.append("Description field cannot be empty!")
        if request.POST['new_td_from'] == '':
            errors.append("Travel Date From field cannot be empty!")
        if request.POST['new_td_to'] == '':
            errors.append("Travel Date To field cannot be empty!")
        if request.POST['new_td_to'] < request.POST['new_td_from']:
            errors.append("Travel End Date must be after Travel Start Date")          
        if len(errors) > 0:
            print 'errors exist'
            for err in errors:
                messages.error(request, err)
            return redirect('/travels/destination/create')
        else:
            newly_planned_trip = Trip.objects.create(
                destination=request.POST['new_destination'], 
                travel_start_date=request.POST['new_td_from'], 
                travel_end_date=request.POST['new_td_to'],
                plan=request.POST['new_description'], 
                travelers_id=request.session['user_id'])
            newly_planned_trip.trip_planner.add(User.objects.get(id=request.session['user_id']))
            print request.POST['new_td_from']
            print request.POST['new_td_to']
    return redirect('/travels')    

def destination(request, id):
    if 'user_id' not in request.session:
        return redirect(reverse("get_main"))
    user_id = request.session['user_id']
    print user_id
    context = {
        'this_trip': Trip.objects.get(id=id),
        'in_their_travel_plans': Trip.objects.get(id=id).trip_planner.all(),
        'test': Trip.objects.get(id=id).trip_planner.exclude(travelers_trips=request.session['user_id']),
    }    
    print context
    return render(request, 'travels/destination.html', context)

def remove_item(request, id):
    Trip.objects.get(id=id).trip_planner.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/travels')

def delete_item(request, id):
    Trip.objects.get(id=id).delete()
    return redirect('/travels')

def add_to_mylist(request, id):
    Trip.objects.get(id=id).trip_planner.add(User.objects.get(id=request.session['user_id']))
    return redirect('/travels')