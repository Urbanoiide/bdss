from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


#FECHA HORARIA
from django.http import JsonResponse
from datetime import datetime

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def saludo_api(request):
    # Obtiene la hora local directamente del sistema operativo
    hora_actual = datetime.now().hour
    
    if hora_actual < 12:
        saludo = "Buenos días!" 
    elif hora_actual < 18:
        saludo = "Buenas tardes!"
    else:
        saludo = "Buenas noches!"
    
    return JsonResponse({"saludo": saludo, "hora": hora_actual})