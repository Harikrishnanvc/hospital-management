from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.models import UserDetails
from .models import Thread


@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    user = UserDetails.objects.filter(user_details__username=request.user)
    guest = UserDetails.objects.all().exclude(user_role=user[0].user_role)
    context = {
        'Threads': threads,
        'user_profile': user,
        'guest': guest
    }
    return render(request, 'chat/messages.html', context)
