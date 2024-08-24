from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ethosapi.models import Score, Profile

class ScoreView(ViewSet):
    """Ethos log view"""

    def retrieve(self, request, pk): 
      """returns a single score by id"""
      try:
        score = Score.objects.get(pk=pk) 
        serializer = ScoreSerializer(score)
        return Response(serializer.data)
      except Score.DoesNotExist as ex: # returns 404 if score doesnt exist
        return Response({'message': 'score not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
      """returns all scores in database with option to filter by profile"""
      scores = Score.objects.all()
      
      profile = request.query_params.get('profile', None)
      if profile is not None:
          scores =  scores.filter(profile_id=profile)
          
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
    
    def update(self, request, pk):
        """Handle PUT requests for a score

        Returns:
            Response -- Empty body with 204 status code
        """

        score = Score.objects.get(pk=pk)
        score.score = request.data["score"]
        score.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        score = Score.objects.get(pk=pk)
        score.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('id', 'score', 'profile')
        # TODO: add depth (in exposing get requests at bottom)