from django.shortcuts import render

def ciaulaweb_home(request):
    return render(request, template_name="home.html")

# sostituibile con
# class HomeView(TemplateView):
#   template_name = 'home.html'

