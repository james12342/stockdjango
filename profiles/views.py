from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# importing messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import User
from ads.models import Author
from ads.models import AdViewerActivity
from ads.models import Ads

from authentication.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from json import dumps
from django.core import serializers


# Model Forms.

# Create your views here.

# Profile Dashboard view
@login_required(login_url='login')
def profile_dashboard(request):
    ads_posted = request.user.author.ads_set.all()
    total_ads = request.user.author.ads_set.all().count()
    featured_ads = request.user.author.ads_set.filter(is_featured=True).count()
    total_earning = 967.98
    adViewerActivity=AdViewerActivity.objects.exclude(AdID=1)

    #print(adViewerActivity)
    ads_posted_json = serializers.serialize("json", ads_posted.all())
    adViewerActivity_json=serializers.serialize("json", adViewerActivity)
    # dump data
    dataJSON_ads = dumps(ads_posted_json)

    context = {
        'ads_posted' : ads_posted,
        'total_ads' : total_ads,
        'total_earning' : total_earning,
        'featured_ads' : featured_ads,
        'data_ads' : dataJSON_ads,
        'data_adViewerActivity' : adViewerActivity_json,
    }
    return render(request, 'profiles/account-dashboard.html', context)
    #return render(request, 'pages/ads_test.html', context)

# Profile Settings view
@login_required(login_url='login')
def profile_settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.author)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your profile has been updated successfully!")
            return redirect('profile-settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.author)

    context = {
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request, 'profiles/account-setting.html', context)

# Profile Ads view
@login_required(login_url='login')
def profile_ads(request):
    return render(request, 'profiles/all-ads.html')

# Profile Favorite Ads view
@login_required(login_url='login')
def profile_favorite_ads(request):
    return render(request, 'profiles/favourite-ads.html')

# Profile Delete view
@login_required(login_url='login')
def profile_close(request):
    return render(request, 'profiles/account-close.html')



