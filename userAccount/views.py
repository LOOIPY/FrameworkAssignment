from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import UserUpdateForm, ProfileUpdateForm, PropertyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from .models import EmailOTP
from django.contrib.auth import get_user_model
from proplistpage.models import Property

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Step 1: Generate or update OTP
            otp_obj, _ = EmailOTP.objects.get_or_create(user=user)
            otp_obj.generate_code()

            # Step 2: Send OTP to user's email
            send_mail(
                subject="Your verification code",
                message=f"Hi {user.username},\n\nYour verification code is: {otp_obj.code}",
                from_email="webmaster@localhost",
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Step 3: Store temporary login state
            request.session['pre_2fa_user_id'] = user.id
            request.session['pre_otp_user_id'] = user.id
            request.session['next'] = request.POST.get("next") or request.GET.get("next", "")

            return redirect('verify_otp')
        else:
            messages.error(request, "Invalid username or password.")

    # ✅ This line must always be present outside the POST block
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

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'accounts/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        next_url = request.POST.get('next') or '/'
        return redirect(next_url)

    next_url = request.GET.get('next', '')
    return render(request, 'accounts/signup.html', {'next': next_url})

def social_redirect_view(request):
    return redirect(request.session.pop('next', '/'))

@login_required
def profile_view(request):
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

def delete_my_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, user=request.user)
    if request.method == 'POST':
        prop.delete()
        return redirect('my_properties')