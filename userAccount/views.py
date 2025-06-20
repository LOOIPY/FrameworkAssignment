from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.utils.http import url_has_allowed_host_and_scheme
=======
from django.http import JsonResponse
from django.views.decorators.http import require_POST
>>>>>>> Pei-Yi
from .forms import UserUpdateForm, ProfileUpdateForm, PropertyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from .models import EmailOTP
from django.contrib.auth import get_user_model
<<<<<<< HEAD
from proplistpage.models import Property
=======
from django.forms import inlineformset_factory
from proplistpage.models import Property, PropertyImage
from django.utils.http import url_has_allowed_host_and_scheme
from django import forms
from django.urls import reverse
>>>>>>> Pei-Yi

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

<<<<<<< HEAD
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Step 1: Generate or update OTP
            otp_obj, _ = EmailOTP.objects.get_or_create(user=user)
            otp_obj.generate_code()

            # Step 2: Send OTP to user's email
=======
        # Check if user exists first
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, "accounts/login.html", {
                'next': request.GET.get('next', '')
            })

        if not user_obj.has_usable_password():
            messages.error(request, "This account uses Google login. Please sign in using Google.")
            return render(request, "accounts/login.html", {
                'next': request.GET.get('next', '')
            })

        # Proceed with password authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # ✅ OTP logic here
            otp_obj, _ = EmailOTP.objects.get_or_create(user=user)
            otp_obj.generate_code()

>>>>>>> Pei-Yi
            send_mail(
                subject="Your verification code",
                message=f"Hi {user.username},\n\nYour verification code is: {otp_obj.code}",
                from_email="webmaster@localhost",
                recipient_list=[user.email],
                fail_silently=False,
            )

<<<<<<< HEAD
            # Step 3: Store temporary login state
            request.session['pre_2fa_user_id'] = user.id
            request.session['pre_otp_user_id'] = user.id
            request.session['next'] = request.POST.get("next") or request.GET.get("next", "")

=======
            request.session['pre_2fa_user_id'] = user.id
            request.session['pre_otp_user_id'] = user.id
            request.session['next'] = request.POST.get("next") or request.GET.get("next", "")
>>>>>>> Pei-Yi
            return redirect('verify_otp')
        else:
            messages.error(request, "Invalid username or password.")

<<<<<<< HEAD
    # ✅ This line must always be present outside the POST block
=======
>>>>>>> Pei-Yi
    return render(request, "accounts/login.html", {
        'next': request.GET.get('next', '')
    })

User = get_user_model()

def verify_otp(request):
    user_id = request.session.get("pre_otp_user_id")

    if not user_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect("login")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        code = request.POST.get("otp")

        otp_obj = EmailOTP.objects.filter(user=user, code=code).first()

        if otp_obj:
            # Manually specify backend if multiple are configured
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            del request.session["pre_otp_user_id"]
            messages.success(request, "OTP verified. You are now logged in.")
            return redirect("/")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "accounts/verify_otp.html")

def resend_otp(request):
    user_id = request.session.get("pre_otp_user_id")
    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect("login")

    user = User.objects.get(id=user_id)

    # regenerate and resend OTP
    otp_obj, _ = EmailOTP.objects.get_or_create(user=user)
    otp_obj.generate_code()

    send_mail(
        subject="Your verification code",
        message=f"Hi {user.username},\n\nYour new verification code is: {otp_obj.code}",
        from_email="webmaster@localhost",
        recipient_list=[user.email],
        fail_silently=False,
    )

    messages.success(request, "A new OTP has been sent to your email.")
    return redirect("verify_otp")

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
<<<<<<< HEAD
=======
        phone_number = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile_picture')
>>>>>>> Pei-Yi

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'accounts/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
<<<<<<< HEAD
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

=======
        user.set_unusable_password()
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        # Update profile
        profile = user.profile
        profile.phone_number = phone_number
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()

>>>>>>> Pei-Yi
        next_url = request.POST.get('next') or '/'
        return redirect(next_url)

    next_url = request.GET.get('next', '')
    return render(request, 'accounts/signup.html', {'next': next_url})

def social_redirect_view(request):
    return redirect(request.session.pop('next', '/'))

@login_required
def profile_view(request):
<<<<<<< HEAD
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # same view
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
=======
    profile = request.user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # If checkbox was checked, remove the profile picture
            if request.POST.get('remove_picture') == 'on':
                if profile.profile_picture:
                    profile.profile_picture.delete(save=False)
                    profile.profile_picture = None
                    profile.save()

            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    referer = request.META.get('HTTP_REFERER')
    fallback_url = reverse('proplistpage:property-list')

    if referer and 'password_change' not in referer and 'profile' not in referer:
        safe_referer = referer
    else:
        safe_referer = fallback_url

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'referer': safe_referer,
>>>>>>> Pei-Yi
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Replace with your profile view name
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'password_change.html', {'form': form})

def my_properties(request):
    properties = Property.objects.filter(user=request.user)
    return render(request, 'accounts/my_properties.html', {'properties': properties})

<<<<<<< HEAD
def add_my_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.user = request.user
            prop.save()
            return redirect('my_properties')
    else:
        form = PropertyForm()
    return render(request, 'accounts/add_my_property.html', {'form': form, 'title': 'Add New Property'})

def edit_my_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            return redirect('my_properties')
    else:
        form = PropertyForm(instance=prop)
    return render(request, 'accounts/edit_my_property.html', {'form': form})

=======
PropertyImageFormSet = inlineformset_factory(
    Property,
    PropertyImage,
    fields=('image', 'caption'),
    extra=1,  # show 3 empty image inputs by default
    can_delete=True,
    widgets={
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'caption': forms.TextInput(attrs={'class': 'form-control'}),
    }
)

@login_required
def add_my_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        formset = PropertyImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            prop = form.save(commit=False)
            prop.user = request.user
            prop.save()
            formset.instance = prop
            formset.save()
            return redirect('my_properties')
    else:
        form = PropertyForm()
        formset = PropertyImageFormSet()

    return render(request, 'accounts/add_my_property.html', {
        'form': form,
        'formset': formset,
        'title': 'Add New Property'
    })

@login_required
def edit_my_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=prop)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('my_properties')
    else:
        form = PropertyForm(instance=prop)
        formset = PropertyImageFormSet(instance=prop)

    return render(request, 'accounts/edit_my_property.html', {
        'form': form,
        'formset': formset,
        'property': prop,
    })
>>>>>>> Pei-Yi
def delete_my_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, user=request.user)
    if request.method == 'POST':
        prop.delete()
<<<<<<< HEAD
        return redirect('my_properties')
=======
        return redirect('my_properties')

@login_required
def toggle_favorite(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    profile = request.user.profile

    if property in profile.favorites.all():
        profile.favorites.remove(property)
    else:
        profile.favorites.add(property)

    # ✅ Redirect to `next` if it's passed and safe
    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)

    # Fallback: go to property detail
    return redirect('proplistpage:property-detail', pk=property_id)

@login_required
def saved_properties(request):
    saved = request.user.profile.favorites.all()
    return render(request, 'accounts/saved_properties.html', {'saved_properties': saved})

@require_POST
@login_required
def ajax_toggle_favorite(request):
    from django.views.decorators.csrf import csrf_exempt
    import json
    data = json.loads(request.body)
    property_id = data.get('property_id')
    property = Property.objects.filter(id=property_id).first()

    if not property:
        return JsonResponse({'error': 'Property not found'}, status=404)

    profile = request.user.profile
    is_favorited = property in profile.favorites.all()

    if is_favorited:
        profile.favorites.remove(property)
    else:
        profile.favorites.add(property)

    return JsonResponse({'favorited': not is_favorited})
>>>>>>> Pei-Yi
