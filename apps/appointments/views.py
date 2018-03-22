from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from ..login.models import User
from .models import Appointments
import datetime
from datetime import date



# =================================================
# 						HELPERS
# =================================================
def current_user(request):

    return User.objects.get(id=request.session['user_id'])


def flash_errors(request, errors):

    for error in errors:

        messages.error(request, error)

# ==============================================================
# 						RENDER
# ==============================================================
def index(request):

    print "in the index"



#CHECK IS THERE IS A USER_ID IN SESSION
    if 'user_id' not in request.session:

# RETURN REDIRECT TO THE INDEX.HTML IF USER_ID NOT IN SESSION
        return redirect('/')

#ELSE SET VARIABLE "USER" TO EQUAL CURRENT_USER // FROM CURRENT_USER HELPER METHOD ABOVE

    user = current_user(request)

    today = datetime.datetime.now().strftime('%Y-%m-%d')

    time = datetime.datetime.now().strftime('%I:%M %p')

    today_app = Appointments.objects.filter(date = today)

    future_app = Appointments.objects.exclude(date = today)

#PASS VARIABLES THROUGH CONTEXT
    context = {
        'user': user,
        'today_app': today_app,
        'future_app': future_app,
        'today': today,
        'time': time,
    }

    return render(request, 'appointments/index.html', context)


def show(request, appoint_id):

    today = datetime.datetime.now().strftime('%Y-%m-%d')

    appointment = Appointments.objects.get(id = appoint_id)

    time = appointment.time.strftime('%I:%M %p')

    context = {

        'appointment' : Appointments.objects.get(id = appoint_id),
        'today': today,
        'time': time,
    }
    

    return render(request, 'appointments/user.html', context)

# =================================================
#                       PROCESS
# =================================================


def edit(request, appoint_id):
    print "========     in the edit   ============"

    Appointments.objects.filter(pk=appoint_id).update(tasks=request.POST['tasks'], status=request.POST['status'], date=request.POST['date'], time=request.POST['time'])


    # request.session['tasks'] = form_data['tasks']
    # request.session['status'] = form_data['status']
    # request.session['date'] = form_data['date']
    # request.session['time'] = form_data['time']
    
    print request.POST['time']

    return redirect('dashboard')

def create(request):
    if request.method == "POST":

        errors = Appointments.objects.validate(request.POST)

        if not errors:
            user = current_user(request)
            Appointments.objects.addAppointment(request.POST, request.session["user_id"])

        flash_errors(request, errors)
    return redirect('dashboard')


def delete(request, appoint_id):

    Appointments.objects.get(id=appoint_id).delete()

    return redirect('dashboard')


def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')

    return redirect(reverse('landing'))