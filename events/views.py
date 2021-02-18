from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class LandingView(TemplateView):
    template_name = 'land.html'
    
    def get(self,request):
        return render(request,LandingView.template_name)