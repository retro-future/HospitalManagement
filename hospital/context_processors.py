def user_profile_picture(request):
    if request.user.is_authenticated:
        user_group = request.user.groups.first()
        if user_group:
            group_name = user_group.name
            profile_pic_attr = {
                'DOCTOR': 'doctor',
                'PATIENT': 'patient',
                'ADMIN': 'administrator'
            }.get(group_name)
            if profile_pic_attr:
                avatar = getattr(request.user, profile_pic_attr).profile_pic
                return {"avatar": avatar}
    return {}