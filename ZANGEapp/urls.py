from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  path('',views.ZangeList.as_view(),name='index'),
  path('login/',views.Login.as_view(),name='login'),
  path('logout/',views.Logout.as_view(),name='logout'),
  path('signup/',views.signup,name='signup'),
  path('post/',views.post_form,name='post'),
  path('detail/<int:pk>/',views.detail,name='detail'),
  path('about/',views.about,name='about'),
  path('link/',views.link,name='link'),
  path('faceshape/', views.image_upload, name='faceshape'),
  path('stack/', views.edinet_search, name='edinet_search'),
  path('result/',views.call_edinet_api,name='call_edinet_api'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)