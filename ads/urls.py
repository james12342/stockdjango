from django.urls import path

from .import views
from rest_framework import routers, serializers, viewsets
from .views import AdsViewSets
from .views import AdsImagesViewSets
from .views import UserViewSets
from .views import AuthorViewSets


from django.urls import path,include


router = routers.DefaultRouter()
router.register('Ads', AdsViewSets)
router.register('AdsImages', AdsImagesViewSets)
router.register('User', UserViewSets)
router.register('Author', AuthorViewSets)




urlpatterns = [

    path('', include(router.urls)),
    path('ads-api/', include(router.urls)),


    path('post-ads/', views.post_ads, name='post-ads'),
    path('add_advieweractivity/', views.Add_AdViewerActivity, name='add_advieweractivity'),
    path('ads-listing/', views.ads_listing, name='ads-listing'),
    path('ads/<int:pk>/', views.ads_detail, name='ads-detail'),
    path('ads/<int:pk>/', views.ads_detail, name='ads-view'),
    
    path('ads/<int:pk>/edit/', views.ads_edit, name='ads-edit'),
    path('ads/<int:pk>/delete/', views.ads_delete, name='ads-delete'),
    path('category/<slug:slug>/', views.ads_category_archive, name='category-archive'),
    path('country/<slug:slug>/', views.ads_country_archive, name='country-archive'),
    
    path('postIPaddress/<slug:slug>/', views.ads_postIPaddress_archive, name='postIPaddress-archive'),
    path('postADViewerIP/<slug:slug>/', views.ads_postADViewerIP_archive, name='postADViewerIP-archive'),

    path('state/<slug:slug>/', views.ads_state_archive, name='state-archive'),
    path('city/<slug:slug>/', views.ads_city_archive, name='city-archive'),
    path('author/<int:pk>/', views.ads_author_archive, name='author-archive'),
    path('ads-search/', views.ads_search, name='ads-search'),

    path('ads/<int:pk>/requestpay/', views.ads_requestPayment, name='ads-requestpay'),

    path('ads-updatepayacc/', views.ads_updatepayacc, name='ads-updatepayacc'),

    path('ads-listing/', views.ads_listing, name='ads-listing'),

    # path('adstest',TemplateView.as_view(template_name='ads_test.html'), name='adstest'),
   
    # path('ads-api/', include(router.urls)),
   
  
]