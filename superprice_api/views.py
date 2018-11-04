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
import base64
from django.core.files.base import ContentFile
import os
from django.conf import settings
from .microservices.arduino import  sendText
from .price import PriceCalculator


def decode_image(data):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)  # You can save this as file instance.
    return data


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['price'] = 1
        context['product'] = "apple"
        return context



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
        imageObj = Images(image=decode_image(request.POST["img"]))
        imageObj.save()
        self.analyze(imageObj.image)
        return HttpResponse('Succeeded')

    @action(detail=False, methods=['post'], name='Analyize an image')
    def analyze(self, image):
        analysis = analyze_image(image.path)
        fruit = None
        list = analysis["description"]["tags"]
        print(list)
        for value in list:
            if (value == "apple"):
                fruit = Fruits.objects.get(title="apple")
                if 'red' in list: #This is very bad!
                    fruit.price /= 2
                break
            elif (value == "banana"):
                fruit = Fruits.objects.get(title="banana")
                break


        if(fruit == None):
            print("Nothing")
            return

        #TODO: Call calculations on fruit and load template

        pricer = PriceCalculator(fruit)
        pricer.calculate_discount()
        pricer.calculate_price()

        #TODO: Update Arduino
        priceString = fruit.title+" ${0:.2f}".format(pricer.price)
        sendText(priceString)





