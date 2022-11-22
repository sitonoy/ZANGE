from django.urls import path
from . import views
from .views import ContactFormView, ContactResultView


urlpatterns = [
  path('',views.ZangeList.as_view(),name='index'),
  path('login/',views.Login.as_view(),name='login'),
  path('logout/',views.Logout.as_view(),name='logout'),
  path('signup/',views.signup,name='signup'),
  path('post/',views.post_form,name='post'),
  path('detail/<int:pk>/',views.detail,name='detail'),
  path('about/',views.about,name='about'),
  path('link/',views.link,name='link'),
  path('contact/', ContactFormView.as_view(), name='contact_form'),
  path('contact/result/', ContactResultView.as_view(), name='contact_result'),
  path('stack/', views.edinet_search, name='edinet_search'),
  path('result/',views.call_edinet_api,name='call_edinet_api'),
]