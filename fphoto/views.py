# -*- coding: ISO-8859-1 -*-

# python imports
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from open_facebook import OpenFacebook


def home(request):
    """ Home page to show login for facebook """

    context = RequestContext(request,
            {'user': request.user})

    return render_to_response('home.html', context_instance=context)


@login_required
def logout(request):
    """ Logout from facebook and django app """

    from django.contrib.auth import logout
    context = RequestContext(request,
            {'user': request.user})

    # logout from facebook
    profile = request.user.get_profile()
    profile.disconnect_facebook()
    profile.save()

    # logout from django app
    logout(request)
    return render_to_response('home.html', context_instance=context)


@login_required
def dash(request):
    """ Show user pics in dashboard """
    context = RequestContext(request,
            {'user': request.user})

    # access token from user profile
    # will be used to access fb
    user_profile = request.user.get_profile()
    facebook = OpenFacebook(user_profile.access_token)

    # get all user uploaded pics from fb
    photos = facebook.get("me/photos/uploaded", fields='images,album')

    # logic to get the smallest image
    # single image and album will be displayed
    display_photos = []
    for photo in photos['data']:
        sorted_images = sorted(photo['images'])
        thumbnail = sorted_images[0]
        large = sorted_images[-1]
        display_photos.append((photo['album'], thumbnail, large))

    context['display_photos'] = display_photos
    return render_to_response('dash.html', context_instance=context)
