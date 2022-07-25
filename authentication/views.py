from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, Http404
# importing messages
from django.contrib import messages
# import authentication related stuffs
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User

from .forms import UserRegistrationForm

from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .tokens import account_activation_token
from ads.models import Ads
import requests

# Create your views here.

# Signup view
def signup_view(request):       
    if request.method == 'POST':
        # fill the form with requested data
        reg_form = UserRegistrationForm(request.POST)

        if reg_form.is_valid():
            instance = reg_form.save(commit=False)
            instance.is_active = False
            instance.save()

            site = get_current_site(request)
            mail_subject = "Confirm your usdtads account"
            message = render_to_string('authentication/confirm-email.html', {
                'user':instance,
                'domain':site.domain,
                'uid':instance.id,
                'token':account_activation_token.make_token(instance)
            })

            to_email = reg_form.cleaned_data.get('email')
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
           # send_mail(mail_subject, message, from_email, to_list, fail_silently=False, )

            # now, need to create automatically an superuser created ad for this register
#just activate this user
            try:
              user = get_object_or_404(User, pk=instance.id)
              user.is_active = True
              user.save()
            except:
              raise Http404("No User found")
    
           
             

      
#end activate the user

            #end create automatically ad for this register
            
            return redirect('signup-success')
                            
    else:
        reg_form = UserRegistrationForm()

    context = {
        'reg_form':reg_form,
    }

    return render(request, 'authentication/signup.html', context)

# Signup success view
def signup_success_view(request):
    return render(request, 'authentication/signup-success.html')

# Activate account view
def account_activate_view(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except:
        raise Http404("No User found")
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return render(request, 'authentication/activate-account.html')
    else:
        return HttpResponse("Invalid activation link. Please contact support.")

# Login view
def login_view(request):
    if request.method == 'POST':
        # Get username
        username = request.POST.get('username')
        # Get password
        password = request.POST.get('password')
        # Check authentication
        user = authenticate(request, username=username, password=password)
        # If user exists log them in
        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next','home')

        # now, need to create automatically an superuser created ad for this register
        #first,get the ads belong to this author
            theauthor=request.user.author
            ads_by_author = Ads.objects.filter(author=theauthor)
        # search
        
            ads_Postbysuper=Ads.objects.filter(adPostBy='Superuser').first()           
            thetitle=getattr(ads_Postbysuper, 'title')
            ads_by_author=ads_by_author.filter(title=thetitle)

            #check if exist the ad already, if not, add it
            if ads_by_author.count()==0 :
            
             theprice=getattr(ads_Postbysuper, 'price')
             print("title:"+thetitle)
             thecategory=getattr(ads_Postbysuper, 'category')
             thecondition=getattr(ads_Postbysuper, 'condition')
             thebrand=getattr(ads_Postbysuper, 'brand')
             thephone=getattr(ads_Postbysuper, 'phone')
             thevideo=getattr(ads_Postbysuper, 'video')
             thecountry=getattr(ads_Postbysuper, 'country')
             thestate=getattr(ads_Postbysuper, 'state')
             thecity=getattr(ads_Postbysuper, 'city')
             
             thepostADPaymentReceiveAccount='Please provide your Payment Account'
             thepostADPaymentTotalReceived=0
             thepostADPaymentReceiveable=0
             thepostADClickPerEarn=getattr(ads_Postbysuper, 'postADClickPerEarn')
             thepostADPaymentReceiveStatus='Not Received Yet'
             thepostADUrl=settings.WEBSITEURL
             theadPostBy='AutoAssigned'
            
           # print("author:"+str(theauthor))
             Ads.objects.create(author=theauthor, 
             title=ads_Postbysuper.title,
             price=theprice,
             category=thecategory,
             condition=thecondition,
             brand=thebrand,
             phone=thephone,
             video=thevideo,
             postADPaymentReceiveAccount=thepostADPaymentReceiveAccount,
             postADPaymentTotalReceived=thepostADPaymentTotalReceived,
             postADPaymentReceiveable=thepostADPaymentReceiveable,
             postADPaymentReceiveStatus=thepostADPaymentReceiveStatus,
             postADUrl=thepostADUrl,
             adPostBy=theadPostBy,
             is_active=True,
             country=thecountry,
             state=thestate,
             city=thecity,
             postADClickPerEarn=thepostADClickPerEarn

             
             )
             print("Create Ad for user ok. going to add images to this ad")
             theads=ads_by_author = Ads.objects.filter(author=theauthor).filter(title=thetitle).first()
             theadsID= getattr(theads, 'id')
             print('the ads id:'+str(theadsID))
            #  addImageToAds(theadsID)
            #  print("Images added to the ads ok")
            else :
             print("this user has assigned ad already")
        #end create automatically ad for this register



            return redirect(redirect_url)
        else:
            # Show error message
            messages.error(request, f"Oops! Username or Password is invalid. Please try again.")

    return render(request, 'authentication/login.html')

# Logout view
def logout_view(request):
    # call logout method
    logout(request)
    return redirect('login')

# Add images to Ads
def addImageToAds(adsID):
    url = "http://localhost:8000/ads-api/AdsImages/"

    payload={'ads': '19'}
    files=[
    ('image',('house4.jpg',open('/C:/Users/james/OneDrive/Desk/house4.jpg','rb'),'image/jpeg'))
    ]
    headers = {
    'Authorization': 'Basic amFtZXM6a2VudHh5XzAx'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
