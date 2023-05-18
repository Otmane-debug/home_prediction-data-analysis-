from .models import House

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ["Id", "Address", "Zip", "Price", "Area", "Room", "Lon", "Lat"]