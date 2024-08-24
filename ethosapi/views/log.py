from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ethosapi.models import Log
from ethosapi.models import User
from ethosapi.models import Profile
from datetime import date

class LogView(ViewSet):
    """Ethos log view"""

    def retrieve(self, request, pk): # returns a single Log by id 
        try:
          log = Log.objects.get(pk=pk) 
          serializer = LogSerializer(log)
          return Response(serializer.data)
        except Log.DoesNotExist as ex: # returns 404 if log doesnt exist
          return Response({'message': 'log not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request): # returns all profiles in database 
        logs = Log.objects.all()
        
        profiles = request.query_params.get('profile', None)
        if profiles is not None:
            logs =  logs.filter(profile_id=profiles)
            
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)
    
    def create(self, request): 
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        profile = Profile.objects.get(id=request.data["profile"])
        creator = User.objects.get(id=request.data["creator"])
        current_date = date.today()

        log = Log.objects.create(
            score_impact=request.data["score_impact"],
            title=request.data["title"],
            description=request.data["description"],
            event_date=request.data["event_date"],
            creator=creator,
            profile=profile,
            log_date = current_date,
        )
        serializer = LogSerializer(log)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        log = Log.objects.get(pk=pk)
        log.title = request.data["title"]
        log.description = request.data["description"]
        log.score_impact = request.data["score_impact"]
        log.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)    


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'creator', 'title', 'description', 'event_date', 'profile', 'score_impact')