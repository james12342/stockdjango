from datetime import datetime
from unicodedata import decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import country
from .models import postIPaddress
from .models import postADViewerIP
from .models import Ads
from django.db.models import Count
# Model Forms.
from .forms import AdsForm
from django.contrib.auth.forms import User
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core.mail import send_mail

# importing messages
from django.contrib import messages

from ads.models import Author

from rest_framework.viewsets import ModelViewSet
from .serializers import AdsSerializer,AdsImagesSerializer,UserSerializer,AuthorSerializer

from django.db.models import Sum

# Create your views here.

# Post ads view
@login_required(login_url='login')

def post_ads(request):
    if request.method == 'POST':
        # Get ad title
        title = request.POST.get('title')

        # Get ad description
        description = request.POST.get('description')

        # Get ad category
        category = request.POST.get('category')
        # Check if the category exists
        category_check = Category.objects.filter(category_name=category).exists()
        if category_check:
            c = Category.objects.get(category_name=category) # Get the category if exists
        else:
            c = Category.objects.create(category_name=category) # Create the category
        
        # Get ad price
        price = request.POST.get('price')
        
        # Get ad condition
        condition = request.POST.get('condition')
        
       # Get user's  PostIPaddress
        PostIPaddress = request.POST.get('postIPaddress')
         # Check if the postIPaddress exists
        postIPaddress_check = postIPaddress.objects.filter(postIPaddress_name=PostIPaddress).exists()
        if postIPaddress_check:
            pipadd = postIPaddress.objects.get(postIPaddress_name=PostIPaddress) # Get the postIPaddress if exists
        else:
            pipadd = postIPaddress.objects.create(postIPaddress_name=PostIPaddress) # Create the postIPaddress

         # Get user's  postADViewerIP
        PostADViewerIP = request.POST.get('postADViewerIP')

         # Check if the postADViewerIP exists
        postADViewerIP_check = postADViewerIP.objects.filter(postADViewerIP_name=PostADViewerIP).exists()
        if postADViewerIP_check:
            ipviewer = postADViewerIP.objects.get(postADViewerIP_name=PostADViewerIP) # Get the postADViewerIP if exists
        else:
            ipviewer = postADViewerIP.objects.create(postADViewerIP_name=PostADViewerIP) # Create the postADViewerIP

        # Get user's living country
        Country = request.POST.get('country')
         # Check if the country exists
        country_check = country.objects.filter(country_name=Country).exists()
        if country_check:
            ctr = country.objects.get(country_name=Country) # Get the country if exists
        else:
            ctr = country.objects.create(country_name=Country) # Create the country
                   
        # Get user's living state
        state = request.POST.get('state')
        # Check if the state exists
        state_check = State.objects.filter(state_name=state).exists()
        if state_check:
            s = State.objects.get(state_name=state) # Get the state if exists
        else:
            s = State.objects.create(state_name=state) # Create the state

        # Get user's living city
        city = request.POST.get('city')
        # Check if the city exists
        city_check = City.objects.filter(city_name=city).exists()
        if city_check:
            ci = City.objects.get(city_name=city) # Get the city if exists
        else:
            ci = City.objects.create(city_name=city) # Create the city

        # Get ad brand
        brand = request.POST.get('brand')

        # Get user's phone
        phone = request.POST.get('phone')

        # Get ad video
        video = request.POST.get('video')

        # Get image files length
        length = request.POST.get('length')

         # Get  postADReceivePaymentMethod
        postADReceivePaymentMethod = request.POST.get('postADReceivePaymentMethod')

         # Get postADPaymentReceiveAccount
        postADPaymentReceiveAccount = request.POST.get('postADPaymentReceiveAccount')

        # Get  PostADUrl
        postADUrl = request.POST.get('postADUrl')

        # Get  PostImageUrl
        postImageUrl = request.POST.get('postImageUrl')

        myDate = datetime.now()
    
       # Give a format to the date
        # Displays something like: Aug. 27, 2017, 2:57 p.m.
        formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")

        # Create the ad
        ads = Ads.objects.create(author=request.user.author, title=title, description=description, price=price, category=c, condition=condition, postIPaddress=pipadd,postADViewerIP=ipviewer,country=ctr,state=s, city=ci, brand=brand, phone=phone, video=video ,postADPaymentReceiveAccount=postADPaymentReceiveAccount ,postADReceivePaymentMethod=postADReceivePaymentMethod,postADPaymentTotalReceived=0,postADPaymentReceiveable=0,postADPaymentReceiveStatus='Not Received Yet',postADPaymentLatestReceiveDate=formatedDate,postImageUrl=postImageUrl,postADUrl=postADUrl)

        # Attach the images with the associated ad
        for file_num in range(0, int(length)):
            AdsImages.objects.create(
                ads=ads,
                image=request.FILES.get(f'images{file_num}')
            )
        
        # Send email notificaton to Admin
        mail_subject = "New Ads submitted"
        sender_email = request.user.email
        message = f"Dear Admin, you received a new ads request from {sender_email}"
        print(message)
        to_email = settings.EMAIL_HOST_USER
        to_list = [to_email]
        from_email = settings.EMAIL_HOST_USER
        
        send_mail(
            mail_subject,
            message,
            from_email,
            to_list,
            fail_silently=False,
        )
        
    return render(request, 'ads/post-ads.html')

# Ads listing view
def ads_listing(request):
    ads_listing = Ads.objects.all()
    category_listing = Category.objects.annotate(total_ads=Count('ads')).order_by('category_name')

    context = {
        'ads_listing' : ads_listing,
        'category_listing' : category_listing
    }

    return render(request, 'ads/ads-listing.html', context)

# Ads detail view
def ads_detail(request, pk):
    ads_detail = get_object_or_404(Ads, pk=pk)
    # check the ads is an assigned ad or superuser created ad, if assigned ad, get the image from the superuser ad
    ads_detail_adpostby=getattr(ads_detail, 'adPostBy')
    if ads_detail_adpostby=='AutoAssigned':
      print('ad is an an auto assgined ad, get the image from the super user created ad')
    # get the superuser created ad
      ads_superuser=Ads.objects.filter(adPostBy='Superuser').first()
      
      ads_superuser_adID=getattr(ads_superuser,'id')
      print('ads_superuser_adID:'+str(ads_superuser_adID))

      ads_photos = AdsImages.objects.filter(ads=ads_superuser)
    else :
      print('ad is super user created ad, get images from itself')
      ads_photos = AdsImages.objects.filter(ads=ads_detail)

    ads_ViewerActivityCount=AdViewerActivity.objects.filter(AdID=pk).count

    context = {
        'ads_detail' : ads_detail,
        'ads_photos' : ads_photos,
        'ads_ViewerActivityCount' : ads_ViewerActivityCount,
    }

    return render(request, 'ads/ads-detail.html', context)

# Ads category archive view
def ads_category_archive(request, slug):
    category = get_object_or_404(Category, slug=slug)
    ads_by_category = Ads.objects.filter(category=category)

    context = {
        'category' : category,
        'ads_by_category' : ads_by_category
    }

    return render(request, 'ads/category-archive.html', context)

# Ads postIPaddress archive view
def ads_postIPaddress_archive(request, slug):
    PostIPaddress = get_object_or_404(postIPaddress, slug=slug)
    ads_by_postIPaddress = Ads.objects.filter(PostIPaddress=PostIPaddress)

    context = {
        'postIPaddress' : PostIPaddress,
        'ads_by_postIPaddress' : ads_by_postIPaddress
    }

    return render(request, 'ads/postIPaddress-archive.html', context)

# Ads postADViewerIP archive view
def ads_postADViewerIP_archive(request, slug):
    PostADViewerIP = get_object_or_404(postADViewerIP, slug=slug)
    ads_by_postADViewerIP = Ads.objects.filter(PostADViewerIP=PostADViewerIP)

    context = {
        'postADViewerIP' : PostADViewerIP,
        'ads_by_postADViewerIP' : ads_by_postADViewerIP
    }

    return render(request, 'ads/postADViewerIP-archive.html', context)

# Ads country archive view
def ads_country_archive(request, slug):
    Country = get_object_or_404(country, slug=slug)
    ads_by_country = Ads.objects.filter(Country=Country)

    context = {
        'country' : Country,
        'ads_by_country' : ads_by_country
    }

    return render(request, 'ads/country-archive.html', context)

# Ads state archive view
def ads_state_archive(request, slug):
    state = get_object_or_404(State, slug=slug)
    ads_by_state = Ads.objects.filter(state=state)

    context = {
        'state' : state,
        'ads_by_state' : ads_by_state
    }

    return render(request, 'ads/state-archive.html', context)

# Ads city archive view
def ads_city_archive(request, slug):
    city = get_object_or_404(City, slug=slug)
    ads_by_city = Ads.objects.filter(city=city)

    context = {
        'city' : city,
        'ads_by_city' : ads_by_city
    }

    return render(request, 'ads/city-archive.html', context)

# Ads author archive view
def ads_author_archive(request, pk):
    author = get_object_or_404(Author, pk=pk)
    ads_by_author = Ads.objects.filter(author=author)

    context = {
        'author' : author,
        'ads_by_author' : ads_by_author
    }

    return render(request, 'ads/author-archive.html', context)

# Ads search/filter view
def ads_search(request):

    state = request.GET.get('state_name')
    category = request.GET.get('category_name')

    if state:
        ads_search_result = Ads.objects.filter(state__state_name=state)
    elif category:
        ads_search_result = Ads.objects.filter(category__category_name=category)
    else:
        ads_search_result = Ads.objects.filter(state__state_name=state).filter(category__category_name=category)
    
    context = {
        'ads_search_result':ads_search_result
    }

    return render(request, 'ads/ads-search.html', context)
#update ad payment account
@login_required(login_url='login')
def ads_updatepayacc(request):
     if request.method == 'POST':
        # Get ad AdID
       theAdID = request.POST.get('AdID')
       
       thepostADReceivePaymentMethod=request.POST.get('postADReceivePaymentMethod')
       thepostADPaymentReceiveAccount=request.POST.get('postADPaymentReceiveAccount')
       
        #theAdID = request.POST.get('viewerCountry')
       print("Update AdID :"+theAdID+"--PaymentMethod:"+thepostADReceivePaymentMethod+"--PaymentReceiveAccount:"+thepostADPaymentReceiveAccount)
       Ads.objects.filter(id=int(theAdID)).update(postADReceivePaymentMethod = thepostADReceivePaymentMethod,postADPaymentReceiveAccount=thepostADPaymentReceiveAccount)
       print("Update AdID :"+theAdID+" payment Account OK")
     return redirect ('dashboard')

#Post AdViewerActivity
def Add_AdViewerActivity(request):
     if request.method == 'POST':
        # Get ad AdID
        theAdID = request.POST.get('AdID')
        #theAdID = request.POST.get('viewerCountry')
        print("########################### AdID is:"+theAdID)
       # get the ad
        #thead=Ads.objects.filter(title='Coca cola')
        #thead=get_object_or_404(Ads, pk=int(theAdID))
        # get the author of this AdID
        theAuthor=Ads.objects.filter(pk=int(theAdID)).first().__getattribute__('author')
        print("########################### theAuthor is:"+str(theAuthor))
        thead=Ads.objects.filter(id=int(theAdID)).first()
        #get the current view count
        theadViewCount=AdViewerActivity.objects.filter(AdID=int(theAdID)).count()
        print("########################### theadViewCount is:"+str(theadViewCount))

         #get the current view pay per click
        field_name = 'postADClickPerEarn'        
        thePayPerClick = getattr(thead, field_name)
        print("########################### thePayPerClick is:"+str(thePayPerClick))

        # caculate the total click earning
        totalClickEarn=thePayPerClick*(theadViewCount+1)
        print("########################### theTotalClickEarn is:"+str(totalClickEarn))
        # Get viewerIP
        theviewerIP = request.POST.get('viewerIP')
        print("########################### theviewerIP is:"+theviewerIP)
        #theviewerIP = '204.13.24.67'

        # Get viewerCountry
        theviewerCountry = request.POST.get('viewerCountry')
        #theviewerCountry = 'USA'

        # Get viewerState
        theviewerState = request.POST.get('viewerState')

        # Get viewerCity
        theviewerCity = request.POST.get('viewerCity')

        # Get viewerZip
        theviewerZip = request.POST.get('viewerZip')

        # Get viewerTimezone
        theviewerTimezone = request.POST.get('viewerTimezone')

        # Get viewerIsp
        theviewerIsp = request.POST.get('viewerIsp')

        # Get viewerLat
        theviewerLat = request.POST.get('viewerLat')

        # Get viewerLon
        theviewerLon = request.POST.get('viewerLon')

        # Get viewerViewTime
        #viewerViewTime
        myDate = datetime.now()
    
    # Give a format to the date
    # Displays something like: Aug. 27, 2017, 2:57 p.m.
        formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")

        theviewerViewTime = request.POST.get('viewerViewTime')
        print("########################### viewerViewTime is:"+theviewerViewTime)

        # Get viewerViewDuration
        theviewerViewDuration = '05/08/2022'
    
       # check the activity list if there are same ip address, if exist, do nothing, if not, add the ip address into activity list
        sameIPCount=AdViewerActivity.objects.filter(viewerIP=theviewerIP ).filter(AdID=theAdID).count()
        print("########################### IP Address:"+str(theviewerIP)+" Count is:"+str(sameIPCount))
        if sameIPCount==0:

        # Create the AdViewerActivity
       # adViewerActivity = AdViewerActivity.objects.create(ads=thead, AdID=theAdID, viewerIP =theviewerIP ,viewerCountry=theviewerCountry,viewerState=theviewerState,viewerCity=theviewerCity,viewerZip=theviewerZip,viewerTimezone=theviewerTimezone,viewerIsp=theviewerIsp,viewerLat=theviewerLat,viewerLon=theviewerLon)
         AdViewerActivity.objects.create(ads=thead, AdID=theAdID, viewerIP =theviewerIP ,viewerCountry=theviewerCountry,viewerState=theviewerState,viewerCity=theviewerCity,viewerZip=theviewerZip,viewerTimezone=theviewerTimezone,viewerIsp=theviewerIsp,viewerLat=theviewerLat,viewerLon=theviewerLon,viewerViewTime=formatedDate,author=theAuthor)
       # print (adViewerActivity)

        # first, check if the master ad is hitting the max earn, if yes, do nothing, else update the count and total earn
         masterADMaxEarn=Ads.objects.filter(adPostBy='Superuser').first().__getattribute__('postADMaxEarn')
         print("########################### Master AD postADMaxEarn is:"+str(masterADMaxEarn))
         AllAdTotalEarn=Ads.objects.aggregate(Sum('postADTotalEarn'))
         print("########################### All ADs postADTotalEarn is:"+str(AllAdTotalEarn['postADTotalEarn__sum']))

        # if All ADs Earn total > master AD max post earn, then do nothing, else update the click counts and total earns
         if AllAdTotalEarn['postADTotalEarn__sum'] -masterADMaxEarn>=0:
          print ("####### postADTotalEarn__sum is over masterADMaxEarn, this AD new count and earning is end")
         else:
          print ("####### postADTotalEarn__sum is less than masterADMaxEarn, Update view counts and total earning")
        #update the view total count in ads table
          Ads.objects.filter(id=int(theAdID)).update(postADClickCount = theadViewCount+1)
        #update the view total earning in the ads table
          Ads.objects.filter(id=int(theAdID)).update(postADTotalEarn = totalClickEarn)
        else:
         print("########################### IP Address:"+str(theviewerIP)+" exist, do nothing")
        return redirect ('dashboard')
    # return render(request, 'ads/post-ads.html')
        #return render(request, 'ads/'+theAdID+'.html')

# Ads delete view
@login_required(login_url='login')
def ads_delete(request, pk):
    ad = get_object_or_404(Ads, pk=pk)
    ad.delete()
    return redirect("dashboard")

# Ads edit view
@login_required(login_url='login')
def ads_edit(request, pk):                                         
    data = get_object_or_404(Ads, pk=pk)
    print (data.description)
    data.description=str(data.description).replace('<p>', '').replace('</p>', '')
    form = AdsForm(instance=data) 
    
    # form.description=str(form.description).replace("<p>","")                                                             

    if request.method == "POST":
        form = AdsForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect ('dashboard')
    context = {
        "editForm":form
    }
    return render(request, 'ads/edit-ads.html',context)

#request payment
def ads_requestPayment(request,pk):
     print('come to request pay id:'+str(pk))
     
        #viewerViewTime
     myDate = datetime.now()
        #update the view total earning in the ads table
     Ads.objects.filter(pk=pk).update(postADPaymentReceiveStatus = "Request payment at:"+str(myDate))
     return redirect ('dashboard')
    
#AdsViewSets
class AdsViewSets(ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer

    #AdsImagesViewSets
class AdsImagesViewSets(ModelViewSet):
    queryset = AdsImages.objects.all()
    serializer_class = AdsImagesSerializer

  #UserViewSets
class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#AuthorViewSets
class AuthorViewSets(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

