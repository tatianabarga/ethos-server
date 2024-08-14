from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from ethosapi.models import Profile, User, Circle, CircleProfile, Score

class ProfileView(ViewSet):
    """Ethos profile view"""

    def retrieve(self, request, pk): 
        """returns a single profile by id"""
        try:
          profile = Profile.objects.get(pk=pk) 
          serializer = ProfileSerializer(profile)
          return Response(serializer.data)
        except Profile.DoesNotExist as ex: # returns 404 if profile doesnt exist
          return Response({'message': 'profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request): 
        """returns all profiles in database with options to filter by creator or circle using query"""
        profiles = Profile.objects.all()
        
        creator_id = request.query_params.get('creator', None)
        if creator_id is not None:
            profiles =  Profile.objects.filter(creator=creator_id)
      
        circle = request.query_params.get('circle', None)
        if circle is not None:
            profiles =  profiles.filter(circleprofile__circle_id=circle)
            
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def create(self, request): 
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        creator = User.objects.get(id=request.data["creator"])
        # score = request.query_params.get('score', None)
        
        serializer = ProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            profile = serializer.save()
            circles = request.data.get('circles', [])
            if not isinstance(circles, list):
                circles = [circles]
                
            # if score is not None:
            #     Score.objects.create(
            #         score = score,
            #         profile = profile
            #     )
                
            # score may need to be created seperately using form on frontend
                
            for circle_id in circles:
                try:
                    circle = Circle.objects.get(pk=circle_id)
                    CircleProfile.objects.create(
                        circle = circle,
                        profile = profile,
                    ) 
                except Circle.DoesNotExist:
                    return Response({'error': f'Circle with id {circle_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.data)
    
    def update(self, request, pk): # TODO:
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        
        profile = Profile.objects.get(pk=pk)
        profile.bio = request.data["bio"]
        profile.name = request.data["name"]
        # profile.circles = request.data["circles"]
        profile.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk): # TODO:
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'creator', 'bio', 'name', 'circles')
        # TODO: add depth (in exposing get requests at bottom)