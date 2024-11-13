from django.shortcuts import render,get_object_or_404,redirect
from .forms import NewsletterForm
from django.contrib import messages
from .models import SubscribedUsers,Events
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from tinymce.widgets import TinyMCE
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from . decorators import user_not_authenticated
from . decorators import user_is_superuser
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# Create your views here.
def events(request):
    events = Events.objects.all() # Rerieve all the events from the database
    return render(request,'events.html',{'events':events})



@user_is_superuser 
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers')
            message = form.cleaned_data.get('message')

            # Split the comma-separated string of receivers into a list
            receivers_list = [receiver.strip() for receiver in receivers.split(',')]

            # Check if the user has a valid email
            user_email = request.user.email if request.user.is_authenticated and request.user.email else 'default@example.com'
            mail = EmailMessage(subject, message, f"Redeemers Church <{user_email}>", bcc=receivers_list)
            mail.content_subtype = 'html'

            if mail.send():
                messages.success(request, "Email sent successfully")
            else:
                messages.error(request, "There was an error sending the email")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        return redirect('event-url')

    form = NewsletterForm()
    # Fetch email addresses of all subscribed users and join them into a comma-separated string
    receivers_initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    form.fields['receivers'].initial = receivers_initial
    return render(request, 'newsletter.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email',None)

        if not email:
            messages.error(request,'Please enter a valid email address to subscibe to our Newsletters!...')
            return redirect('event-url')
        if get_user_model().objects.filter(email=email).first():
            messages.error(request,f'found registerd user with associated {email} email.You must login to subscribe or the unsubscibe')
            return redirect(request.META.get('HTTP_REFERER','event-url'))
        
        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request,f'{email} email address is already a subscriber')
            return redirect(request.META.get('HTTP_REFERER','event-url'))
        
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request,e.messages[0])
            return redirect('event-url')
        

        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.email = email
        subscribe_model_instance.save()

        messages.success(request,f'{email} email was susccessfully subscribe to our neswletter!...')
        return redirect(request.META.get('HTTP_REFERER','event-url')) 
    

def contact(request):
    if request.method == 'POST':
        message_name = request.POST['name']
        message_email =  request.POST['email']
        message = request.POST['message']

        # function to send the email
        send_mail(
            message_name,
            message,
            message_email,
            ['ondeyostephen0@gmail.com']
        )
        return render(request,'contact.html',{'message_name':message_name})
    return render(request,'contact.html')

