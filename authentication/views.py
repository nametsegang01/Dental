from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.conf import settings
from twilio.rest import Client
from django.conf import settings

# Landing page
def landing(request):
    return render(request, "authentication/landingpage.html")

# Home page
@login_required(login_url='signin')
def home(request):
    return render(request, "authentication/index.html")

# Signup page
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists please try some other username")
            return redirect('home')
    
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('home')

        myuser = User.objects.create_user(username=username, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your account has been successfully created.")
        return redirect('signin')
    
    return render(request, "authentication/signup.html")

        

# Signin page
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    return redirect('/')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment  # your model
from django.contrib.auth.decorators import login_required

@login_required
def book(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes')

        # Save appointment without created_at
        Appointment.objects.create(
            user=request.user,
            full_name=full_name,
            date=date,
            time=time,
            notes=notes
        )

        # Add success message
        messages.success(request, f"Appointment successfully booked for {date} at {time}!")

        # Redirect to dashboard
        return redirect('dashboard')  # adjust if your dashboard URL name is different

    return render(request, 'book.html')


from django.shortcuts import render

from django.utils import timezone
from .models import Appointment  # import your model if not already

def dashboard(request):
    appointments = Appointment.objects.filter(user=request.user, date__gte=timezone.now()).order_by('date')
    return render(request, 'dashboard.html', {'appointments': appointments})

from django.contrib.auth import logout
from django.shortcuts import redirect

def signout(request):
    logout(request)
    return redirect('landing')

from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    appointment.delete()
    messages.success(request, "Your appointment has been canceled.")
    return redirect('dashboard')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')


def team(request):
    return render(request, 'team.html')

def tips(request):
    return render(request, 'tips.html')

from django.shortcuts import render, redirect
from .models import Testimonial
from .forms import TestimonialForm
from django.contrib import messages

def testimonials(request):
    testimonials = Testimonial.objects.order_by('-created_at')[:10]  # show latest 10
    form = TestimonialForm()
    return render(request, 'testimonials.html', {'testimonials': testimonials, 'form': form})

def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your feedback!")
        else:
            messages.error(request, "There was an error submitting your testimonial.")
    return redirect('testimonials')
