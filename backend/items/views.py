from django.shortcuts import render

# Create your views here.

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from items.models import Item
from items.serializers import ItemSerializer
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def all_items(request):
    if request.method == 'GET':
        items = Item.objects.all()
        
        product_id = request.query_params.get('product_id', None)
        if product_id is not None:
            items = items.filter(product_id__icontains=product_id)
        item_serializer = ItemSerializer(items, many=True)
        return JsonResponse(item_serializer.data, safe=False)
         
    elif request.method == 'POST':
        item_data = JSONParser().parse(request)
        item_serializer = ItemSerializer(data=item_data)
        if item_serializer.is_valid():
            item_serializer.save()
            added_item = Item.objects.get(product_id = item_data['product_id'])
            add_to_update_sheet(added_item, added_item)
            return JsonResponse(item_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Item.objects.all().delete()
        return JsonResponse({'message': '{} Deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
