from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ethosapi.models import User, Circle, CircleProfile, Profile, CircleUser

class CircleView(ViewSet):
    """Ethos profile view"""

    def retrieve(self, request, pk): 
        """returns a single circle by id"""
        try:
          profile = Circle.objects.get(pk=pk) 
          serializer = CircleSerializer(profile)
          return Response(serializer.data)
        except Circle.DoesNotExist as ex: # returns 404 if profile doesnt exist
          return Response({'message': 'circle not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """returns all circles in database"""
        circles = Circle.objects.all()
            
        profile = request.query_params.get('profile', None)
        user = request.query_params.get('user', None)
        
        if profile is not None:
            circles =  circles.filter(circleprofile__profile_id=profile)
            
        if user is not None:
            circles =  circles.filter(circleuser__user_id=user)
            
        serializer = CircleSerializer(circles, many=True)
        return Response(serializer.data)
    
    def create(self, request): 
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        serializer = CircleSerializer(data=request.data)
        
        creator = User.objects.get(pk=request.data["creator"])
        
        if serializer.is_valid():
            circle = serializer.save()
            users = request.data.get('users', [])
            if not isinstance(users, list):
                users = [users]
            for user_id in users:
                try:
                    user = User.objects.get(pk=user_id)
                    CircleUser.objects.create(
                        circle = circle,
                        user = user,
                    ) 
                except User.DoesNotExist:
                    return Response({'error': f'user with id {user_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        """Handle PUT requests for a circle

        Returns:
            Response -- Empty body with 204 status code
        """

        circle = Circle.objects.get(pk=pk)
        circle.name = request.data["name"]
        
        joins = CircleUser.objects.filter(circle_id=pk)
        old_user_ids = joins.values_list('user_id', flat=True)
        new_users = request.data["users"]
        
        if old_user_ids != new_users: # if the circles field has changed
            for user in old_user_ids: # find any deleted circles
                if user not in new_users:
                    # pull instance from join table and delete 
                    joins.filter(user_id=user).delete()
                
            for user in new_users: # find any added circles
                if user not in old_user_ids:
                    # create instance in join table 
                    new_user = User.objects.get(pk=user)
                    CircleUser.objects.create(
                        user = new_user,
                        circle = circle,
                    ) 
                    
        circle.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        circle = Circle.objects.get(pk=pk)
        circle.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = '__all__'