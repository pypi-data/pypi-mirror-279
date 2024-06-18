from django.urls import include, path
from custom_urls.bread_urls import BREAD_URLS

# Maybe you want this to be customizable
urlpatterns = [
    path(r'orm/bread/', include(BREAD_URLS))
]
