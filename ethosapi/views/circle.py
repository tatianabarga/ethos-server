from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ethosapi.models import User, Circle

class CircleView(ViewSet):
    """Ethos profile view"""

    def retrieve(self, request, pk): # returns a single profile by id
        try:
          profile = Profile.objects.get(pk=pk) 
          serializer = ProfileSerializer(profile)
          return Response(serializer.data)
        except Profile.DoesNotExist as ex: # returns 404 if profile doesnt exist
          return Response({'message': 'profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request): # returns all profiles in database 
        circles = Circle.objects.all()
        
        # creator_id = request.query_params.get('creator', None)
        # if creator_id is not None:
        #     profiles =  profiles.filter(creator=creator_id)
      
        # circle = request.query_params.get('circle', None)
        # if circle is not None:
        #     profiles =  profiles.filter(circle=circle) # TODO: test - will this work if the profile has multiple circles?
            
        serializer = CircleSerializer(circles, many=True)
        return Response(serializer.data)
    
    def create(self, request): 
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        creator = User.objects.get(pk=request.data["creator"])
        print(creator.name)

        # circle = Circle.objects.create(
        #     name=request.data["name"],
        #     creator=creator,
        # )
        
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
        circle = Circle.objects.get(pk=pk)
        circle.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ('id', 'creator', 'name')