# your_app_name/context_processors.py

def user_info(request):
    user_info = {}
    if request.user.is_authenticated:
        user_info['first_name'] = request.user.first_name
        user_info['last_name'] = request.user.last_name
        user_info['email'] = request.user.email
        user_info['id'] = request.user.id
        # Include any other user-related data you need
    return {'user_info': user_info}
