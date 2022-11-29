from rest_framework import serializers

from location.models import Location
from location.serializers import LocationPostSerializer
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    total_ads = serializers.SerializerMethodField()

    def get_total_ads(self, obj):
        return obj.user_ad.filter(is_published=True).count()

    class Meta:
        model = User
        depth = 1
        fields = '__all__'


class UserPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = LocationPostSerializer()

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location, _ = Location.objects.get_or_create(**location_data)
        return User.objects.create(location=location, **validated_data)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'role', 'age', 'location')


# Кажется можно сделать проще, я put и patch в один сериализатор затолкал
class UserUpdateSerializer(serializers.ModelSerializer):
    location = LocationPostSerializer(required=False)

    def is_valid(self, raise_exception=False):
        self.location_data = self.initial_data.pop('location', None)
        super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        location_data = self.validated_data.pop('location', None)
        super().update(instance=instance, validated_data=validated_data)
        if self.location_data:
            location, created = Location.objects.get_or_create(**self.location_data)
            if created:
                instance.location = location
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'role', 'age', 'location')


class UserDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',)
