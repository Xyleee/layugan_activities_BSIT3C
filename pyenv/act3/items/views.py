from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Sample data - this will be our "database" for this exercise
items = [
    {"id": 1, "name": "Ballpen", "description": "Pilot tech-pen", "price": 15},
    {"id": 2, "name": "Pencil", "description": "Mongol 2", "price": 10},
    {"id": 3, "name": "Notebook", "description": "A5 size", "price": "22"},
]

# Helper function to get the next available ID
def get_next_id():
    return max(item["id"] for item in items) + 1 if items else 1

# GET /api/items/ - Return all items or filter by search parameter
@csrf_exempt
def get_items(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        filtered_items = [item for item in items if search_query.lower() in item["name"].lower()]
        return JsonResponse(filtered_items, safe=False)
    
    return JsonResponse(items, safe=False)

# GET /api/items/<int:item_id>/ - Get a single item
@csrf_exempt
def get_item(request, item_id):
    for item in items:
        if item["id"] == item_id:
            return JsonResponse(item)
    
    return JsonResponse({"error": "Item not found"}, status=404)

# POST /api/items/add/ - Add a new item
@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        try:
            # Try to parse JSON data first
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                # Otherwise, use form data
                data = {
                    "name": request.POST.get("name"),
                    "description": request.POST.get("description"),
                    "price": float(request.POST.get("price", 0))
                }
            
            # Create new item with next available ID
            new_item = {
                "id": get_next_id(),
                "name": data["name"],
                "description": data["description"],
                "price": data["price"]
            }
            
            items.append(new_item)
            return JsonResponse(new_item, status=201)
        
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

# PUT /api/items/update/<int:item_id>/ - Update an item
@csrf_exempt
def update_item(request, item_id):
    if request.method == 'PUT':
        try:
            # Try to parse JSON data first
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                # Otherwise, use form data
                data = {
                    "name": request.POST.get("name"),
                    "description": request.POST.get("description"),
                    "price": float(request.POST.get("price", 0))
                }
            
            # Find and update the item
            for i, item in enumerate(items):
                if item["id"] == item_id:
                    items[i].update({
                        "name": data.get("name", item["name"]),
                        "description": data.get("description", item["description"]),
                        "price": data.get("price", item["price"])
                    })
                    return JsonResponse(items[i])
            
            return JsonResponse({"error": "Item not found"}, status=404)
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Only PUT method is allowed"}, status=405)

# DELETE /api/items/delete/<int:item_id>/ - Delete an item
@csrf_exempt
def delete_item(request, item_id):
    if request.method == 'DELETE':
        for i, item in enumerate(items):
            if item["id"] == item_id:
                deleted_item = items.pop(i)
                return JsonResponse({"message": f"Item {item_id} deleted successfully", "item": deleted_item})
        
        return JsonResponse({"error": "Item not found"}, status=404)
    
    return JsonResponse({"error": "Only DELETE method is allowed"}, status=405)