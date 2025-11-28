def user_info(request):
    if request.user.is_authenticated:
        return {
            'is_superuser': request.user.is_superuser,
        }
    
    return {}