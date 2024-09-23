from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from ..models import Room

@api_view(['GET'])
def getRoutes(requests):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(requests):
    rooms = Room.objects.all()
    serialized = RoomSerializer(rooms, many=True)
    return Response(serialized.data)

@api_view(['GET'])
def getRoom(requests, pk):
    room = Room.objects.get(id=pk)
    serialized = RoomSerializer(room, many=False)
    return Response(serialized.data)