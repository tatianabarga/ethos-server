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
        creator = User.objects.get(pk=request.data["creator"])
        print(creator.name)
        
        serializer = CircleSerializer(data=request.data)
        
        
        if serializer.is_valid():
            circle = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk): # TODO:
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]

        game_type = GameType.objects.get(pk=request.data["gameType"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk): # TODO:
        circle_id = request.query_params.get('id', None)
        circle = Circle.objects.get(pk=pk)
        
        profile_joins = CircleProfile.objects.all()
        profile_joins = profile_joins.filter(circle_id=pk)
        
        # edit circle property on related profiles:
        profiles = [join.profile_id for join in profile_joins]
        
        for profile_id in profiles:
            profile = Profile.objects.get(pk=profile_id)
            profile_circles = profile.circles
            profile_circles.remove(circle_id)
            profile.save() 
        
        profile_joins.delete() # delete circle profile joins
        
        user_joins = CircleUser.objects.all()
        user_joins = user_joins.filter(circle_id=circle)
        user_joins.delete()
        
        circle.delete() # delete circle itself
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ('id', 'creator', 'name')