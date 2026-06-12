from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def chat_view(request):
    chat_group = ChatGroup.objects.filter(group_name__in=["public-chat", "public_chat"]).first()
    if not chat_group:
        chat_group = ChatGroup.objects.first() or ChatGroup.objects.create(group_name="public-chat")

    # Handle Standard POST (Non-HTMX fallback)
    if request.method == "POST" and not request.htmx:
        message_body = request.POST.get("message", "").strip()
        if message_body:
            groupMessage.objects.create(
                group=chat_group,
                author=request.user,
                body=message_body,
            )
            return redirect('home') # Adjust to your actual home URL name

    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    
    # Get other users in this chat
    other_users = User.objects.filter(
        groupmessage__group=chat_group
    ).exclude(id=request.user.id).distinct()

    # Handle HTMX AJAX requests safely
    if request.htmx and request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.group = chat_group
            new_message.author = request.user
            new_message.save()
            
            context = {
                'message' : new_message,  # 👈 Fixed: changed from 'message' to 'new_message'
                'user' : request.user,
            }
            # 👈 Fixed: changed from redirect() to render() for your partial layout
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)

    return render(request, 'a_rtchat/chat.html', {'chat_messages': chat_messages, 'form': form, 'other_users': other_users})