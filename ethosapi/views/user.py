from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ethosapi.models import User

class UserView(ViewSet):
  def retrieve(self, request, pk): # TODO:
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
          
  def list(self, request): # TODO:
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

  def update(self, request, pk): # TODO:
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    name = request.data.get("name", user.name)
    user.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)

    
  def destroy(self, request, pk): # TODO:
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'uid']
        depth = 2