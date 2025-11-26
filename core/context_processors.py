def user_group_flags(request):
    is_manager = False
    if request.user.is_authenticated:
        is_manager = ( request.user.is_superuser or request.user.groups.filter(name="Manager").exists())

    return {"is_manager":is_manager}