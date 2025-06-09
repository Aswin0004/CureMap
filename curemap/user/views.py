from urllib import request
from django.shortcuts import render # type: ignore
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile,FamilyMember
from django.core.files.base import ContentFile
import base64
from django.http import HttpResponseBadRequest
from datetime import date, datetime





# Create your views here.
def homepage(request):
    return render(request, 'userpage/homeindex.html')


@login_required
def user_profile(request):
    # Prevent duplicate profile creation
    if hasattr(request.user, 'user_profile'):
        return redirect('edit_user_profile')
    profile_exists = hasattr(request.user, 'userprofile')

    if profile_exists:
        profile = request.user.userprofile
    else:
        profile = None
    if request.method == 'POST':
        # Handle cropped image
        cropped_data = request.POST.get('cropped_photo')
        photo_file = None

        if cropped_data:
            try:
                format, imgstr = cropped_data.split(';base64,')
                ext = format.split('/')[-1].lower()
                allowed_extensions = ['jpeg', 'jpg', 'png']
                if ext not in allowed_extensions:
                    return HttpResponseBadRequest("Only JPEG, JPG, and PNG images are allowed.")
                
                # Optional: base64 size limit (~5MB)
                if len(imgstr) > 7_000_000:
                    return HttpResponseBadRequest("Image too large.")
                
                photo_file = ContentFile(base64.b64decode(imgstr), name=f'cropped_photo.{ext}')
            except Exception:
                return HttpResponseBadRequest("Invalid image data.")

        # Extract and validate other fields
        middle_name = request.POST.get('middle_name')
        blood_group = request.POST.get('blood_group')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob_raw = request.POST.get('dob') or None
        house_name = request.POST.get('house_name')
        street = request.POST.get('street')
        place = request.POST.get('place')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        # Parse and validate date of birth
        try:
            dob = datetime.strptime(dob_raw, "%Y-%m-%d").date() if dob_raw else None
        except ValueError:
            return HttpResponseBadRequest("Invalid date format for DOB.")

        # Validate phone number and pincode
        if phone_number and not phone_number.isdigit():
            return HttpResponseBadRequest("Phone number should contain only digits.")
        if pincode and not pincode.isdigit():
            return HttpResponseBadRequest("Pincode should contain only digits.")

        # Validate and convert family member count
        try:
            family_member_count = int(request.POST.get('selected_family_members') or 0)
        except ValueError:
            family_member_count = 0

        # Save user profile
        profile = UserProfile(
            user=request.user,
            middle_name=middle_name,
            blood_group=blood_group,
            phone_number=phone_number,
            gender=gender,
            dob=dob,
            house_name=house_name,
            street=street,
            place=place,
            district=district,
            state=state,
            pincode=pincode,
            family_member_count=family_member_count,
            photo=photo_file
        )
        profile.save()

        return redirect('user_profile')  # Redirect to profile page or success view
    
    age = None
    if profile and profile.dob:
        today = date.today()
        age = today.year - profile.dob.year - ((today.month, today.day) < (profile.dob.month, profile.dob.day))

    
    context = {
        'age': age,
        'has_profile': hasattr(request.user, 'userprofile'),
        'family_member_count': request.user.userprofile.family_member_count if hasattr(request.user, 'userprofile') else 0,
}



    return render(request, 'userpage/user_profile.html', context)

@login_required
def register_family_member(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('some_error_page_or_home')

    current_count = FamilyMember.objects.filter(user=user).count()
    can_add_more = current_count < profile.family_member_count

    if request.method == 'POST':
        if not can_add_more:
            messages.error(request, "You have reached the maximum number of allowed family members.")
            return redirect('register_family_member')

        name = request.POST.get('name')
        relationship = request.POST.get('relationship')
        custom_relationship = request.POST.get('custom_relationship')
        photo = request.FILES.get('photo')

        # Use custom relationship if selected
        final_relationship = relationship if relationship != 'Other' else custom_relationship

        if not final_relationship:
            messages.error(request, "Please specify the relationship.")
            return redirect('register_family_member')

        # Create new FamilyMember
        FamilyMember.objects.create(
            user=user,
            name=name,
            relationship=final_relationship,
            photo=photo
        )

        messages.success(request, "Family member added successfully.")
        return redirect('register_family_member')

    context = {
        'can_add_more': can_add_more,
        'current_count': current_count,
        'max_count': profile.family_member_count,
    }
    return render(request, 'userpage/user_profile.html',context)

def add_family_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        relationship = request.POST.get('relationship')
        custom_relationship = request.POST.get('custom_relationship')
        photo = request.FILES.get('photo')

        actual_relationship = custom_relationship if relationship == 'Other' else relationship

        FamilyMember.objects.create(
            user=request.user,
            name=name,
            relationship=relationship,
            custom_relationship=custom_relationship if relationship == 'Other' else '',
            photo=photo
        )
        return redirect('user_profile')

    return render(request, 'userpage/add_family_member.html')

@login_required
def edit_user_profile(request):

    if hasattr(request.user, 'user_profile'):
        return redirect('edit_user_profile')  # or any page you want

    if request.method == 'POST':
        # Read all fields manually from request.POST and request.FILES
        middle_name = request.POST.get('middle_name')
        blood_group = request.POST.get('blood_group')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')  # format: 'YYYY-MM-DD'
        house_name = request.POST.get('house_name')
        street = request.POST.get('street')
        place = request.POST.get('place')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        family_member_count = request.POST.get('family_member_count')
        photo = request.FILES.get('photo')  # For image upload

        # Create the profile instance
        profile = UserProfile(
            user=request.user,
            middle_name=middle_name,
            blood_group=blood_group,
            phone_number=phone_number,
            gender=gender,
            dob=dob if dob else None,
            house_name=house_name,
            street=street,
            place=place,
            district=district,
            state=state,
            pincode=pincode,
            family_member_count=family_member_count or 0,
            photo=photo,
        )
        profile.save()
        return redirect('user_profile')  # replace with your success page

    return render(request, 'userpage/edit_profile.html')

