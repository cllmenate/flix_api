from rest_framework import serializers
from actors.models import Actor


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'  # or specify fields like ('id', 'name', 'age', etc.)
        read_only_fields = ('id',)  # if you want to make the id field read-only
