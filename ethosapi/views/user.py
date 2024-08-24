from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from ethosapi.models import User, Circle, CircleUser

class UserView(ViewSet):
    def retrieve(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
          
          
    def list(self, request):
        users = User.objects.all()
               
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)  
         
  
    def create(self, request):
   
        user = User.objects.create(
            name=request.data["name"],
            uid=request.data["uid"]
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)   
        

    def update(self, request, pk): # TODO: test this
        user = User.objects.get(pk=pk)
        user.name = request.data.get("name", user.name)
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'], url_path='remove-circle/(?P<circle_id>[^/.]+)')
    def remove_circle(self, request, pk, circle_id):
        join = CircleUser.objects.get(user_id=pk, circle_id=circle_id)
        join.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    @action(detail=True, methods=['patch'], url_path='add-circle/(?P<circle_id>[^/.]+)')
    def add_circle(self, request, pk, circle_id):
        circle = Circle.objects.get(pk=circle_id)
        user = User.objects.get(pk=pk)
        CircleUser.objects.create(
            circle = circle,
            user = user,
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    
    def destroy(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'uid', 'circles']
        depth = 2