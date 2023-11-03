from django.shortcuts import render
from .models import Component
from .consumers import ComponentConsumer

def component_list(request):
    components = Component.objects.all()
    return render(request, 'warehouse/component_list.html', {'components': components})

def update_component(request, component_id):
    # Update the component in the database

    # Notify clients about the update
    ComponentConsumer.notify_clients_about_update()