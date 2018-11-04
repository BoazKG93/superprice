from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse, HttpResponseForbidden
from django import forms
# Create your views here.
from .models import Fruits, Images
from .serializers import FruitsSerializer, ImagesSerializers
from rest_framework import viewsets
from rest_framework.decorators import action
from .microservices.azure import analyze_image


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['price'] = 1
        context['product'] = "apple"
        return context


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image',)

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class FruitsView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    queryset = Fruits.objects.all()
    serializer_class = FruitsSerializer

class ImagesView(viewsets.ModelViewSet):

    queryset = Images.objects.all()
    serializer_class = ImagesSerializers

    @action(detail=False, methods=['post'], name='Upload an image')
    def upload(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            self.analyze(image)
            return HttpResponse('Did not find a fruit')
        return HttpResponseForbidden('Form is not valid')

    @action(detail=False, methods=['post'], name='Analyize an image')
    def analyze(self, image):
        analysis = analyze_image(image.image.path)
        fruit = None
        for value in analysis["tags"]:
            if (value["name"] == "apple" and value["confidence"] > 0.4):
                fruit = Fruits.objects.get(title="apple")
                break
            elif (value["name"] == "banana" and value["confidence"] > 0.4):
                fruit = Fruits.objects.get(title="banana")
                break
            else:
                #Do face analysis
                return

        #Call calculations on fruit and load template

        #Update Arduino






