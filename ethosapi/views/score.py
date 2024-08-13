from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ethosapi.models import Score, Profile

class ScoreView(ViewSet):
    """Ethos log view"""

    def retrieve(self, request, pk): # returns a single Log by id # TODO:
        try:
          log = Log.objects.get(pk=pk) 
          serializer = LogSerializer(log)
          return Response(serializer.data)
        except Log.DoesNotExist as ex: # returns 404 if log doesnt exist
          return Response({'message': 'log not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request): # returns all profiles in database # TODO: 
        scores = Score.objects.all()
        
        # profiles = request.query_params.get('profile', None)
        # if profiles is not None:
        #     logs =  logs.filter(profile_id=profiles)
            
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)
    
    def create(self, request): 
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        profile = Profile.objects.get(id=request.data["profile"])

        score_obj = Score.objects.create(
            score=request.data["score"],
            profile=profile,
        )
        serializer = ScoreSerializer(score_obj)
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
        


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('id', 'score', 'profile')
        # TODO: add depth (in exposing get requests at bottom)