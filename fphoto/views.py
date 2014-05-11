from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    context = RequestContext(request,
            {'user': request.user})

    return render_to_response('home.html', context_instance=context)


def logout(request):
    from django.contrib.auth import logout
    context = RequestContext(request,
            {'user': request.user})

    profile = request.user.get_profile()
    profile.disconnect_facebook()
    profile.save()

    logout(request)
    return render_to_response('home.html', context_instance=context)


def dash(request):
    context = RequestContext(request,
            {'user': request.user})

    # access token from user profile
    # will be used to access fb
    from open_facebook import OpenFacebook

    user_profile = request.user.profile_or_self()
    facebook = OpenFacebook(user_profile.access_token)

    photos = facebook.get("me/photos/uploaded", fields='images,album')

    display_photos = []
    for photo in photos['data']:
        thumbnail = sorted(photo['images'])[0]
        display_photos.append((photo['album'], thumbnail))

    context['display_photos'] = display_photos
    return render_to_response('dash.html', context_instance=context)
