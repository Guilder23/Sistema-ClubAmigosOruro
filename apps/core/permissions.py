def can_manage_inventory(user):
    if not getattr(user, 'is_authenticated', False):
        return False
    if user.is_staff:
        return True
    return user.groups.filter(name='operador').exists()
