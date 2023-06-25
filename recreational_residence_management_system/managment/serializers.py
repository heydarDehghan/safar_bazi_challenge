from django.db.models.functions import Abs
from rest_framework import serializers
from managment.models import Booking, Residence, StandardCapacityDetail, ExtraCapacityDetail


# Define the serializers for the models
class StandardCapacityDetailSerializer(serializers.ModelSerializer):
    # A serializer for the standard capacity detail model that shows all fields
    class Meta:
        model = StandardCapacityDetail
        fields = '__all__'


class ExtraCapacityDetailSerializer(serializers.ModelSerializer):
    # A serializer for the extra capacity detail model that shows all fields
    class Meta:
        model = ExtraCapacityDetail
        fields = '__all__'


class ResidenceSerializer(serializers.ModelSerializer):
    # A serializer for the residence model that shows the name, description, and nested serializers for the related models
    standard_capacity_detail = StandardCapacityDetailSerializer()
    extra_capacity_detail = ExtraCapacityDetailSerializer()

    class Meta:
        model = Residence
        fields = ['name', 'description', 'standard_capacity_detail', 'extra_capacity_detail']

    def create(self, validated_data):
        # Get the nested data from the validated data
        standard_capacity_detail_data = validated_data['standard_capacity_detail']
        extra_capacity_detail_data = validated_data['extra_capacity_detail']
        standard_capacity_detail = StandardCapacityDetail.objects.create(**standard_capacity_detail_data)
        extra_capacity_detail = ExtraCapacityDetail.objects.create(**extra_capacity_detail_data)

        validated_data['standard_capacity_detail'] = standard_capacity_detail
        validated_data['extra_capacity_detail'] = extra_capacity_detail
        # Create the residence instance with the remaining data
        residence = Residence.objects.create(**validated_data)
        # Create the related instances with the nested data and associate them with the residence

        # Return the residence instance
        return residence

    def update(self, instance, validated_data):
        # Get the nested data from the validated data

        standard_capacity_detail_data = validated_data['standard_capacity_detail']
        extra_capacity_detail_data = validated_data['extra_capacity_detail']

        # Update the residence instance with the remaining data
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.save()
        # Update or create the related instances with the nested data and associate them with the residence
        standard_capacity_detail, _ = StandardCapacityDetail.objects.update_or_create(
            id=instance.standard_capacity_detail.id,
            defaults=standard_capacity_detail_data)
        extra_capacity_detail, _ = ExtraCapacityDetail.objects.update_or_create(id=instance.extra_capacity_detail.id,
                                                                                defaults=extra_capacity_detail_data)
        # Return the residence instance
        return instance


class ReservationSerializer(serializers.Serializer):
    residence_id = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    extra_adult_num = serializers.IntegerField()
    extra_child_num = serializers.IntegerField()
    extra_baby_num = serializers.IntegerField()


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'


class FilterSerializer(serializers.Serializer):
    adult_num = serializers.IntegerField()
    child_num = serializers.IntegerField()
    baby_num = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()


class FreeResidenceSerializer(serializers.ModelSerializer):
    adult_number_difference = serializers.IntegerField()
    child_number_difference = serializers.IntegerField()
    baby_number_difference = serializers.IntegerField()
    standard_total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Residence
        exclude = ['create_data', 'update_data']

    def get_total_price(self, obj):
        # A function that calculates the duration of the booking in days
        extra_adult_num = obj.adult_number_difference if obj.adult_number_difference > 0 else 0
        extra_child_num = obj.child_number_difference if obj.child_number_difference > 0 else 0
        extra_baby_num = obj.baby_number_difference if obj.baby_number_difference > 0 else 0
        extra_price = obj.extra_capacity_detail.extra_adult_price * extra_adult_num + obj.extra_capacity_detail.extra_child_price * extra_child_num + obj.extra_capacity_detail.extra_baby_price * extra_baby_num
        interval = self.context.get('interval')
        extra_total_price = interval * extra_price
        return obj.standard_total_price + extra_total_price
