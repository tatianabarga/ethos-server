from ethosapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST']) # get?
def check_user(request):
   
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'uid': user.uid,
            'name': user.name
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new Users for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    user = User.objects.create(
        uid=request.data['uid'],
        name=request.data['name']
    )

    # Return the users info to the client
    data = {
        'id': user.id,
        'uid': user.uid,
        'name': user.name
    }
    return Response(data)