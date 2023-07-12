from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from slugify import slugify
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileModelForm
from blog.models import Post

@login_required(login_url='user:login_view')
def user_fav_view(request):
    ids=request.user.userpostfav_set.filter(is_deleted=False).values_list('post_id', flat=True).order_by('-update_at')
    
    context = dict(
        title='Favorilerim',
        favs=Post.objects.filter(id__in=ids, is_active=True)
    )
    return render(request,'blog/post_list.html', context)



@login_required(login_url='user:login_view')
def profile_edit_view(request):
    user = request.user
    initial_data = dict(
        first_name = user.first_name,
        last_name = user.last_name
    )
    form = ProfileModelForm(instance=user.profile, initial = initial_data)
    
    if request.method == 'POST':
        form = ProfileModelForm(
            request.POST or None, 
            request.FILES or None, 
            instance=user.profile
        )
        if form.is_valid():
            f = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            f.save()
            messages.success(request, 'Profil Güncellendi')
            return redirect('user:profile_edit_view')    
    title = 'Profili Düzenle :'
    context = dict(
        form=form,
        title=title,
    )
    return render(request, 'common_components/form.html', context)


def login_view(request):
    #login olan kullanıcı anasayfaya gitsin
    if request.user.is_authenticated:
        messages.info(request,'Daha Önce Login Oldun')
        return redirect('home_view')
    
    context = dict()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        #Bu bilgileri doğru aldık mı
        if len(username) < 6 or len(password) < 6:
            messages.warning(request,'Doğru Gir')
            return redirect('user_profile:login_view')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            #logini kullanıcya belli et
            messages.success(request,'Login Oldun')
            return redirect('home_view')
    return render(request, 'user_profile/login.html', context)


def logout_view(request):
    messages.success(request,'Logout Oldun')
    logout(request)
    return redirect('home_view')


def register_view(request):
    context = dict()
    if request.method == 'POST':
        post_info = request.POST
        email = post_info.get('email')
        email_confirm = post_info.get('email_confirm')
        password = post_info.get('password')
        password_confirm = post_info.get('password_confirm')
        first_name = post_info.get('first_name')
        last_name = post_info.get('last_name')
        instagram = post_info.get('instagram')
        
        if len(first_name) < 3 or len(last_name) < 3 or len(email) < 3 or len(password) < 3:
            messages.warning(request,'En Az 3 Karakter Girin')
            return redirect('user_profile:register_view')

        if email != email_confirm:
            messages.warning(request,'Doğru Mail Gir')
            return redirect('user_profile:register_view')

        if password != password_confirm:
            messages.warning(request,'Doğru Password Gir')
            return redirect('user_profile:register_view')    
       
        user, created = User.objects.get_or_create(username=email)
        if not created:
            user_login = authenticate(request, username=email, password=password)
            if user is not None:
                messages.success(request, "Kayıtlısın, Anasayfaya")
                login(request,user_login)
                return redirect('home_view')  
            messages.warning(request, f'{email} kayıtlı ama login olmadın')
            return redirect('user_profile:login_view')

        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)

        profile, profile_created = Profile.objects.get_or_create(user=user)
        profile.instagram = instagram
        profile.slug = slugify(f"{first_name}-{last_name}") 
        user.save()
        profile.save()
        messages.success(request, f'{user.first_name} Kayıt işlemi tamamlandı')
        user_login = authenticate(request, username=email, password=password)
        login(request, user_login)
        return redirect('home_view')

    return render(request,'user_profile/register.html', context)
    