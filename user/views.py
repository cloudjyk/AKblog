from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import auth, messages
from django.db.models import Count
from django.core.paginator import Paginator
from .models import User, Post, Comment
from .forms import RegForm, LoginForm, PostForm
import os, json
from PIL import Image
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.

def index(request, page=1):
    context = {}
    context['title'] = 'Indexpage'
    if not request.user.is_authenticated:
        messages.error(request, 'Please login first!')
        return HttpResponseRedirect('/login')
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            post_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            post = Post(body=body, post_time=post_time, author=request.user)
            post.save()
            # messages.success(request,'Posted successfully!')
    # context['guser'] = request.user
    followeds = list(map(lambda x:x[0], list(request.user.followeds.values_list('id'))))
    posts = Post.objects.filter(author__in = followeds).order_by('post_time')[::-1]
    posts = Paginator(posts, 3)
    context['posts_all'] = posts
    context['posts'] = posts.page(page)
    print(dir(context['posts']))
    return render(request, 'index.html', context)



def login(request):
    context = {}
    context['title'] = 'Welcome!'
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username = username, password=password) or User.objects.filter(email = username, password=password):
                if username.find('@'):
                    user = auth.authenticate(username=username, password=password)
                else:
                    user = auth.authenticate(email=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    user.last_seen = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    user.save()
                    return HttpResponseRedirect('/index')
            else:
                messages.error(request, 'Wrong username or password!')
    form = RegForm()
    context['form'] = form
    return render(request, 'login.html', context)


def register(request):
    context = {}
    context['title'] = 'Join us!'
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    if request.POST:
        form = RegForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data['username'], form.cleaned_data['password'], form.cleaned_data['email'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            if not form.name_check():
                messages.error(request, 'Username should only include letters and nums, and less than 20 chars.')
                return render(request, 'register.html', context=context)
            if User.objects.filter(username=username):
                messages.error(request, 'Sorry this username is already occupied.')
                return render(request, 'register.html', context=context)
            if User.objects.filter(email=email):
                messages.error(request, 'Sorry this email has already been used by another customer.')
                return render(request, 'register.html', context=context)
            # User.objects.create(username=username, password=password, email=email)
            user = User(username=username, password=password, email=email)
            user.save()
            user.followers.add(user)
            user.save()
            messages.success(request, 'Account created successfully! Join us now~')
            return HttpResponseRedirect('/login')
    else:
        form = RegForm()
        context['form'] = form
    return render(request, 'register.html', context=context)




def user(request, username, page=1):
    context = {}
    context['title'] = 'Homepage'
    if not request.user.is_authenticated:
        messages.error(request, 'Please login first!')
        return HttpResponseRedirect('/login')
    user = User.objects.filter(username = username)[0]
    if not user:
        messages.error(request, 'This user doesn\'t exists!')
        return HttpResponseRedirect('/login')
    context['user'] = user
    posts = Post.objects.filter(author=user).order_by('post_time')[::-1]
    posts = Paginator(posts, 3)
    context['posts_all'] = posts
    context['posts'] = posts.page(page)
    return render(request, 'user.html', context)

def edit(request):
    context = {}
    context['title'] = 'Edit your profile'
    if request.user.is_authenticated:
        guser = User.objects.get(username = request.user.username)
        # auth.logout(request)
        # print(request.user.password)
        # auth.logout(request)
        # print(BASE_DIR)
        # avatar_dir = os.path.join(BASE_DIR, 'static', 'avatars')
        # print(avatar_dir)
        if request.FILES.get('avatar_file'):
            # 本地上传
            avatar_file = request.FILES.get('avatar_file')
            avatar_dir = os.path.join(BASE_DIR, 'static', 'avatars')
            temp_file = os.path.join(avatar_dir,'temp')
            avatar_filename = os.path.join(avatar_dir,guser.username + os.path.splitext(avatar_file.name)[-1])
            print(avatar_filename)
            # 保存上传的文件
            with open(temp_file, 'wb') as f:
                for chunk in avatar_file.chunks():
                    f.write(chunk)
            # 裁剪图片
            top = int(float(request.POST.get('avatar_y')))
            height = int(float(request.POST.get('avatar_height')))
            buttom = top + height
            left = int(float(request.POST.get('avatar_x')))
            width = int(float(request.POST.get('avatar_width')))
            right = left + width

            # python2.7 pillow

            im = Image.open(temp_file)
            # 裁剪图片
            crop_im = im.convert("RGBA").crop((left, top, right, buttom)).resize((width, width), Image.ANTIALIAS)

            # 设置背景颜色为白色
            out = Image.new('RGBA', crop_im.size, (255, 255, 255))
            out.paste(crop_im, (0, 0, width, width), crop_im)

            # 保存图片
            out.save(avatar_filename)
            os.remove(temp_file)
            guser.avatar = avatar_filename.replace(BASE_DIR,'').replace('\\','/')
            guser.save()
        return render(request, 'edit.html', context)



    # context['message'] = 'You have to login first'
    return HttpResponseRedirect('/login')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')

def popular(request, page=1):
    context = {}
    context['title'] = 'Popular users!'
    if not request.user.is_authenticated:
        messages.error(request, 'Please login first!')
        return HttpResponseRedirect('/login')
    userlist = User.objects.annotate(num = Count('followers')).order_by('-num')
    userlist = Paginator(userlist, 4)
    context['users_all'] = userlist
    context['userlist'] = userlist.page(page)
    return render(request, 'popular.html', context)

def follow(request):
    req = json.loads(request.body.decode('utf-8'))
    # req = {}
    # req['username'] = request.POST.get('username')
    print('========', req)
    info = {}
    if req.get('username'):
        if User.objects.filter(username=req['username']):
            user = User.objects.filter(username=req['username'])[0]
            user.followers.add(request.user)
            user.save()
            res = request.user.followeds.count()-1
            info['Meta'] = {'RetCode':200, 'Error':''}
            info['Data'] = res
        else:
            msg = 'Wrong username'
            info['Meta'] = {'RetCode': 400, 'Error': msg}
            info['Data'] = []
    else:
        msg = 'Wrong request'
        info['Meta'] = {'RetCode': 400, 'Error': msg}
        info['Data'] = []
    return JsonResponse(info)

def unfollow(request):
    req = json.loads(request.body.decode('utf-8'))
    # req = {}
    # req['username'] = request.POST.get('username')
    print('========', req)
    info = {}
    if req.get('username'):
        if User.objects.filter(username=req['username']):
            user = User.objects.filter(username=req['username'])[0]
            user.followers.remove(request.user)
            user.save()
            res = request.user.followeds.count()-1
            info['Meta'] = {'RetCode':200, 'Error':''}
            info['Data'] = res
        else:
            msg = 'Wrong username'
            info['Meta'] = {'RetCode': 400, 'Error': msg}
            info['Data'] = []
    else:
        msg = 'Wrong request'
        info['Meta'] = {'RetCode': 400, 'Error': msg}
        info['Data'] = []
    return JsonResponse(info)

def thumbup(request):
    req = json.loads(request.body.decode('utf-8'))
    # req = {}
    # req['username'] = request.POST.get('username')
    print('========', req)
    info = {}
    if req.get('username'):
        if User.objects.filter(username=req['username']):
            user = User.objects.filter(username=req['username'])[0]
            user.thumbupeds.add(request.user)
            user.save()
            res = user.thumbupeds.count()
            info['Meta'] = {'RetCode':200, 'Error':''}
            info['Data'] = res
        else:
            msg = 'Wrong username'
            info['Meta'] = {'RetCode': 400, 'Error': msg}
            info['Data'] = []
    elif req.get('postid'):
        if Post.objects.filter(id=int(req['postid'])):
            post = Post.objects.filter(id=int(req['postid']))[0]
            post.thumbupeds.add(request.user)
            post.save()
            res = post.thumbupeds.count()
            info['Meta'] = {'RetCode':200, 'Error':''}
            info['Data'] = res
        else:
            msg = 'Wrong postid'
            info['Meta'] = {'RetCode': 400, 'Error': msg}
            info['Data'] = []
    else:
        msg = 'Wrong request'
        info['Meta'] = {'RetCode': 400, 'Error': msg}
        info['Data'] = []
    return JsonResponse(info)

def post_comment(request):
    req = json.loads(request.body.decode('utf-8'))
    # req = {}
    # req['username'] = request.POST.get('username')
    print('========', req)
    info = {}
    if req.get('postid') and req.get('comment'):
        if Post.objects.filter(id=int(req['postid'])):
            post = Post.objects.filter(id=int(req['postid']))[0]
            time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            comment = Comment(body=req['comment'],comment_time=time_now,author=request.user,post=post)
            comment.save()
            res = post.comments.count()
            info['Meta'] = {'RetCode':200, 'Error':''}
            info['Data'] = res
        else:
            msg = 'Wrong username'
            info['Meta'] = {'RetCode': 400, 'Error': msg}
            info['Data'] = []
    else:
        msg = 'Bad request'
        info['Meta'] = {'RetCode': 400, 'Error': msg}
        info['Data'] = []
    return JsonResponse(info)

def del_post(request):
    req = json.loads(request.body.decode('utf-8'))
    # req = {}
    # req['username'] = request.POST.get('username')
    print('========', req)
    info = {}
    if req.get('postid'):
        if Post.objects.filter(id=int(req['postid'])):
            post = Post.objects.filter(id=int(req['postid']))[0]
            post.delete()
            res = request.user.posts.count()
            info['Meta'] = {'RetCode': 200, 'Error': ''}
            info['Data'] = res
        else:
            msg = 'Wrong postid'
            info['Meta'] = {'RetCode': 400, 'Error': msg}
            info['Data'] = []
    else:
        msg = 'Bad request'
        info['Meta'] = {'RetCode': 400, 'Error': msg}
        info['Data'] = []
    return JsonResponse(info)

