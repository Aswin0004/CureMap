from urllib import request
from django.forms import modelformset_factory
from django.shortcuts import render # type: ignore
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FamilyMemberForm

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

    familymembers = FamilyMember.objects.all()
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
        'familymembers':familymembers,
}



    return render(request, 'userpage/user_profile.html', context)


def add_family_member(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    # Get existing family members
    existing_members = FamilyMember.objects.filter(user=user)
    existing_count = existing_members.count()

    # Calculate how many more family members the user can add
    allowed_count = profile.family_member_count
    remaining = max(0, allowed_count - existing_count)

    print("existing_count:", existing_count)
    print("allowed_count:", allowed_count)
    print("remaining:", remaining)

    # Always render at least 1 form if the user hasn't reached the limit
    FamilyMemberFormSet = modelformset_factory(
        FamilyMember,
        form=FamilyMemberForm,
        extra=remaining,
        max_num=allowed_count,
        can_delete=False
    )

    if request.method == 'POST':
        formset = FamilyMemberFormSet(request.POST, request.FILES, queryset=existing_members)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = user
                instance.save()
            return redirect('user_profile')  # Update with your success view
    else:
        formset = FamilyMemberFormSet(queryset=existing_members)


    return render(request, 'userpage/add_family_member.html', {
        'formset': formset,
        'max_count': allowed_count,
        'remaining': remaining
    })

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

