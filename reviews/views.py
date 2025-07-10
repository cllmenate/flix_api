from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from reviews.models import Review
from reviews.serializers import ReviewSerializer


# Create your views here.
class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        # Automatically set the movie field if not provided
        if 'movie' not in self.request.data:
            serializer.save(movie=self.request.movie)
        else:
            serializer.save()


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_update(self, serializer):
        # Automatically set the movie field if not provided
        if 'movie' not in self.request.data:
            serializer.save(movie=self.request.movie)
        else:
            serializer.save()
