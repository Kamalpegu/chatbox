from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import *
from .forms import *

User = get_user_model()

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group, created = ChatGroup.objects.get_or_create(group_name=chatroom_name)

    other_user = None

    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break


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



    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            chat_group.members.add(request.user)


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

    context = {
        'chat_messages' : chat_messages, 
        'form' : form,
        'other_user' : other_user,
        'chatroom_name' : chatroom_name,
        'chat_group' : chat_group
    }

    return render(request, 'a_rtchat/chat.html', context)


def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username = username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    
    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private = True)
                chatroom.members.add(other_user, request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private = True)
        chatroom.members.add(other_user, request.user)
        
    return redirect('chatroom', chatroom.group_name)


@login_required
def create_groupchat(request):
    form = NewGroupForm()
    
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)
    
    context = {
        'form': form
    }
    return render(request, 'a_rtchat/create_groupchat.html', context)

@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    can_manage_chatroom = request.user == chat_group.admin
    
    if not can_manage_chatroom and request.user not in chat_group.members.all():
        raise Http404()
    
    form = ChatRoomEditForm(instance=chat_group) 
    
    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            
            if can_manage_chatroom:
                remove_members = request.POST.getlist('remove_members')
                for member_id in remove_members:
                    member = User.objects.get(id=member_id)
                    chat_group.members.remove(member)  
                
            return redirect('chatroom', chatroom_name) 
    
    context = {
        'form' : form,
        'chat_group' : chat_group,
        'can_manage_chatroom' : can_manage_chatroom,
    }   
    return render(request, 'a_rtchat/chatroom_edit.html', context)


@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    if request.method == "POST":
        chat_group.delete()
        messages.success(request, 'Chatroom deleted')
        return redirect('home')
    
    return render(request, 'a_rtchat/chatroom_delete.html', {'chat_group':chat_group})        


@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user not in chat_group.members.all():
        raise Http404()
    
    if request.method == "POST":
        was_admin = request.user == chat_group.admin
        chat_group.members.remove(request.user)
        chat_group.users_online.remove(request.user)
        
        if was_admin:
            next_admin = chat_group.members.first()
            if next_admin:
                chat_group.admin = next_admin
                chat_group.save(update_fields=['admin'])
            else:
                chat_group.delete()
                messages.success(request, 'Chatroom deleted')
                return redirect('home')
        
        messages.success(request, 'You left the Chat')
        return redirect('home')
    
    return render(request, 'a_rtchat/chatroom_leave.html', {'chat_group': chat_group})


def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    
    if request.method != "POST" or 'file' not in request.FILES:
        return HttpResponse(status=400)
    
    uploaded_file = request.FILES['file']
    message = groupMessage.objects.create(
        file=uploaded_file,
        author=request.user,
        group=chat_group,
    )
    
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            chat_group.group_name,
            {
                'type': 'message_handler',
                'message_id': message.id,
            }
        )
    
    return HttpResponse()