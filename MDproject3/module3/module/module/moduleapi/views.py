from rest_framework import viewsets
from rest_framework import permissions
from module.moduleapi.models import MyProjectStock, MyProjectWeather, Savestockprice, Savestockratio
from module.moduleapi.serializers import MyProjectStockSerializer, MyProjectWeatherSerializer, SavestockpriceSerializer, SavestockratioSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class MyProjectStockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyProjectStock.objects.all()
    serializer_class = MyProjectStockSerializer

    permission_classes = [permissions.IsAuthenticated]

    # /my_topic_MyProjectWeather/search?q=test5
    @action(detail=False, methods=['GET'])
    def search(self, request):
        q = request.query_params.get('q', None) 

        qs = self.get_queryset().filter(title=q)
        serializer = self.get_serializer(qs, many=True)
        
        return Response(serializer.data)


class MyProjectWeatherViewSet(viewsets.ModelViewSet):
    queryset = MyProjectWeather.objects.all()
    serializer_class = MyProjectWeatherSerializer

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def search(self, request):
        q = request.query_params.get('q', None) 

        qs = self.get_queryset().filter(title=q)
        serializer = self.get_serializer(qs, many=True)
        
        return Response(serializer.data)

class  SavestockratioViewSet(viewsets.ModelViewSet):
    queryset =  Savestockratio.objects.all()
    serializer_class =  SavestockratioSerializer

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def search(self, request):
        q = request.query_params.get('q', None) 

        qs = self.get_queryset().filter(stock_title=q)
        serializer = self.get_serializer(qs, many=True)
        
        return Response(serializer.data)

class SavestockpriceViewSet(viewsets.ModelViewSet):
    queryset = Savestockprice.objects.all()
    serializer_class = SavestockpriceSerializer

    permission_classes = [permissions.IsAuthenticated]

    # @action(detail=False, methods=['GET'])
    # def search(self, request):
    #     q = request.query_params.get('q', None) 

    #     qs = self.get_queryset().filter(stock_title=q)
    #     serializer = self.get_serializer(qs, many=True)
        
    #     return Response(serializer.data)
    