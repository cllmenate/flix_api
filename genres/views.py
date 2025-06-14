import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from genres.models import Genre

# Create your views here.
@csrf_exempt
def genre_create_list_view(request):
    if request.method == 'GET':
        genres = get_object_or_404(Genre.objects.all())
        data = [{'id': genre.id, 'name': genre.name, 'description': genre.description} for genre in genres]
        
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        description = data.get('description', '')
        if not name:
            return JsonResponse({'message': 'Name is required'}, status=400)
        genre = Genre(name=name, description=description)
        genre.save()
        return JsonResponse({'id': genre.id, 'name': genre.name, 'description': genre.description}, 
                            status=201)
    
    # Retorne um erro para métodos não suportados
    return JsonResponse({'message': 'Method not allowed'}, 
                        status=405)

@csrf_exempt
def genre_detail_view(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == 'GET':
        data = {
            'id': genre.id,
            'name': genre.name,
            'description': genre.description
        }
        return JsonResponse(data)

    # Handles updating an existing genre.
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        if 'name' in data:
            genre.name = data['name']
        if 'description' in data:
            genre.description = data['description']
        if not genre.name:
            return JsonResponse({'message': 'Name is required'}, 
                                status=400)
        genre.save()
        return JsonResponse({'id': genre.id, 'name': genre.name, 'description': genre.description})

    elif request.method == 'DELETE':
        genre.delete()
        return JsonResponse({'message': 'Genre deleted successfully'}, 
                            status=204)

    return JsonResponse({'message': 'Method not allowed'}, 
                        status=405)