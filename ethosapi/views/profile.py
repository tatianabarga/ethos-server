from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ethosapi.models import Profile
from ethosapi.models import User

class ProfileView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk): # returns a single profile by id
        try:
          profile = Profile.objects.get(pk=pk) 
          serializer = ProfileSerializer(profile)
          return Response(serializer.data)
        except Profile.DoesNotExist as ex: # returns 404 if profile doesnt exist
          return Response({'message': 'profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request): # returns all profiles in database 
        profiles = Profile.objects.all()
        
        creator_id = request.query_params.get('creator_id', None)
        if creator_id is not None:
            profiles =  profiles.filter(creator_id=creator_id)
      
        circle = request.query_params.get('circle', None)
        if circle is not None:
            profiles =  profiles.filter(circle_id=circle) # TODO: test - will this work if the profile has multiple circles?
            
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def create(self, request): 
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        creator = User.objects.get(id=request.data["creator_id"])
        
        # TODO: add create initial score logic
        # TODO: add circles logic

        profile = Profile.objects.create(
            name=request.data["name"],
            bio=request.data["bio"],
            creator_id=creator,
        )
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
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
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'creator_id', 'bio', 'name')
        # fields = ('id', 'creator_id', 'bio', 'name', 'score_id', 'circles')
        # TODO: add depth (in exposing get requests at bottom)