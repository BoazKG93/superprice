from .views import FruitsView, ImagesView, IndexView
from django.urls import path

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("fruits", FruitsView)
router.register("images", ImagesView, base_name="ImagesView")

urlpatterns = [
    path('', IndexView.as_view(), name='indexview'),
]

urlpatterns += router.urls
