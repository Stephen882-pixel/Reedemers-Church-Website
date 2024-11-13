from django.urls import path
from .import views

urlpatterns = [
    path('events',views.events,name='event-url'),
    path('contact',views.contact,name='contact-url'),
    path('newsletter',views.newsletter,name='newsletter-url'),
    path('newsletter_subscription',views.subscribe,name='newsletter_subscription_url'),
]
