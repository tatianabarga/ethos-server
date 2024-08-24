from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from ethosapi.models import Profile, User, Circle, CircleProfile, Score, Log

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
        
        serializer = ProfileSerializer(data=request.data)
        
        
        if serializer.is_valid():
            profile = serializer.save()
            circles = request.data.get('circles', [])
            score = request.data.get('score', None)
            if not isinstance(circles, list):
                circles = [circles]
                
            if score is not None:
                Score.objects.create(
                    score = score,
                    profile = profile,
                ) 
                
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
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        
        profile = Profile.objects.get(pk=pk)
        profile.bio = request.data["bio"]
        profile.name = request.data["name"]
        
        joins = CircleProfile.objects.all()
        joins = joins.filter(profile_id=pk)
        
        old_circles = list(profile.circles.all())
        old_circle_ids = []
         
        for circle in old_circles:
            id = circle.id
            old_circle_ids.append(id)
        
        new_circles = request.data["circles"]
        
        if old_circle_ids != new_circles: # if the circles field has changed
            for circle in old_circle_ids: # find any deleted circles
                if circle not in new_circles:
                    # pull instance from join table and delete 
                    joins.filter(circle_id=circle).delete()
                
            for circle in new_circles: # find any added circles
                if circle not in old_circle_ids:
                    # create instance in join table 
                    new_circle = Circle.objects.get(pk=circle)
                    CircleProfile.objects.create(
                        circle = new_circle,
                        profile = profile,
                    ) 
                    
            profile.circles.set(new_circles)
        profile.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk): # TODO:
        profile = Profile.objects.get(pk=pk)
        
        score = Score.objects.get(profile=pk)
        score.delete() # delete score
        
        
        joins = CircleProfile.objects.all()
        joins = joins.filter(profile_id=pk)
        joins.delete()# delete joins for profile from circleprofile table
        
        logs = Log.objects.all()
        logs = logs.filter(profile_id=pk)
        logs.delete() # delete logs for profile
        
        profile.delete() #delete profile itself
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'creator', 'bio', 'name', 'circles')
        # TODO: add depth (in exposing get requests at bottom)