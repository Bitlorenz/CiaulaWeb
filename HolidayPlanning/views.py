from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Questa è la view della parte in cui si organizza la vacanza")
