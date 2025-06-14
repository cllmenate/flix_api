from django.http import JsonResponse
from genres.models import Genre

# Create your views here.
def genre_view(request):
    genres = Genre.objects.all()
    data = [{'id': genre.id, 'name': genre.name, 'description': genre.description} for genre in genres]
    if not data:
        return JsonResponse({'message': 'No genres found'}, status=404)
    return JsonResponse(data, safe=False)