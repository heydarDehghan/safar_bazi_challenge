from datetime import datetime, timedelta

from django.db.models import Q, ExpressionWrapper, F, DecimalField, Value
from django.db.models.functions import Abs
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.fields import DateTimeField
from rest_framework.response import Response
from managment.models import Residence, StandardCapacityDetail, ExtraCapacityDetail, Booking
from managment.serializers import BookingSerializer, ResidenceSerializer, StandardCapacityDetailSerializer, \
    ExtraCapacityDetailSerializer, FilterSerializer, FreeResidenceSerializer, ReservationSerializer

from managment.basic_functions import calculate_total_booking_price


# Define the viewsets for the models
class ResidenceViewSet(viewsets.ModelViewSet):
    # A viewset for the residence model that allows CRUD operations and uses the residence serializer
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Override the create method to check for uniqueness before creating an instance
        # Get the request data
        data = request.data
        # Get the name from the data
        name = data.get('name')
        # Try to find an existing instance with the same name
        try:
            instance = Residence.objects.get(name=name)
            # If found, update the instance with the new data and save it
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Residence.DoesNotExist:
            # If not found, create a new instance as usual
            return super().create(request, *args, **kwargs)


class StandardCapacityDetailViewSet(viewsets.ModelViewSet):
    # A viewset for the standard capacity detail model that allows CRUD operations and uses the standard capacity detail serializer
    queryset = StandardCapacityDetail.objects.all()
    serializer_class = StandardCapacityDetailSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Override the create method to check for uniqueness before creating an instance
        # Get the request data
        data = request.data
        # Get the residence id from the data
        residence_id = data.get('residence')
        # Get the capacity details from the data
        adult_number = data.get('adult_number')
        child_number = data.get('child_number')
        baby_number = data.get('baby_number')
        # Try to find an existing instance with the same residence and capacity details
        try:
            instance = StandardCapacityDetail.objects.get(
                residence=residence_id,
                adult_number=adult_number,
                child_number=child_number,
                baby_number=baby_number
            )
            # If found, update the instance with the new data and save it
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except StandardCapacityDetail.DoesNotExist:
            # If not found, create a new instance as usual
            return super().create(request, *args, **kwargs)


class ExtraCapacityDetailViewSet(viewsets.ModelViewSet):
    # A viewset for the extra capacity detail model that allows CRUD operations and uses the extra capacity detail serializer
    queryset = ExtraCapacityDetail.objects.all()
    serializer_class = ExtraCapacityDetailSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Override the create method to check for uniqueness before creating an instance
        # Get the request data
        data = request.data
        # Get the residence id from the data
        residence_id = data.get('residence')
        # Get the price details from the data
        extra_adult_price = data.get('extra_adult_price')
        extra_child_price = data.get('extra_child_price')
        extra_baby_price = data.get('extra_baby_price')
        # Try to find an existing instance with the same residence and price details
        try:
            instance = ExtraCapacityDetail.objects.get(
                residence=residence_id,
                extra_adult_price=extra_adult_price,
                extra_child_price=extra_child_price,
                extra_baby_price=extra_baby_price
            )
            # If found, update the instance with the new data and save it
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ExtraCapacityDetail.DoesNotExist:
            # If not found, create a new instance as usual
            return super().create(request, *args, **kwargs)


@api_view(['POST'])
def booking(request):
    try:
        if request.method == 'POST':

            serializer = ReservationSerializer(data=request.data)
            if serializer.is_valid():
                start_date = serializer.validated_data['start_date']
                end_date = serializer.validated_data['end_date']
                residence_id = serializer.validated_data['residence_id']
                extra_adult_num = serializer.validated_data['extra_adult_num']
                extra_child_num = serializer.validated_data['extra_child_num']
                extra_baby_num = serializer.validated_data['extra_baby_num']
                residence = Residence.objects.get(pk=residence_id)

                if end_date <= start_date or start_date < datetime.now(start_date.tzinfo) + timedelta(days=1):
                    return Response(data={'error_message': 'The timeframe is not properly selected'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if residence is None:
                    return Response(data={'error_message': 'There is no residence with this specifications'},
                                    status=status.HTTP_404_NOT_FOUND)

                # Checking that the residence is free in the requested period
                items = Booking.objects.filter(residence_id=residence_id, is_canceled=False,
                                               start_date__range=(start_date, end_date),
                                               end_date__range=(start_date, end_date),
                                               )
                # Filter items based on paid or less than 2 hours since booking
                items = items.filter(Q(payment_status=1) | Q(create_data__range=(
                    datetime.now(start_date.tzinfo) - timedelta(hours=2), datetime.now(start_date.tzinfo))))

                if items.count() == 0:
                    booking_residence = Booking(residence_id=residence.id,extra_adult_num=extra_adult_num,extra_child_num=extra_child_num,extra_baby_num=extra_baby_num,
                                                start_date=start_date, end_date=end_date)

                    booking_residence.total_price, booking_residence.standard_total_price = calculate_total_booking_price(
                        residence.standard_capacity_detail,
                        residence.extra_capacity_detail ,
                        extra_adult_num,
                        extra_child_num,
                        extra_baby_num,
                        end_date,
                        start_date)
                    booking_residence.save()

                    serializer = BookingSerializer(booking_residence)

                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                return Response(data={'message': 'An item with this profile is not available'},
                                status=status.HTTP_200_OK)
            return Response(data={'error_messages': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def free_residence_list(request):
    try:
        if request.method == 'GET':

            serializer = FilterSerializer(data=request.data)
            if serializer.is_valid():
                start_date = serializer.validated_data['start_date']
                end_date = serializer.validated_data['end_date']
                adult_num = serializer.validated_data['adult_num']
                child_num = serializer.validated_data['child_num']
                baby_num = serializer.validated_data['baby_num']

                interval = (end_date - start_date).days

                if end_date <= start_date:
                    return Response(data={'error_message': 'The timeframe is not properly selected'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Checking that the residence is free in the requested period
                items = Booking.objects.filter(
                    is_canceled=False,
                    start_date__gt=datetime.now(),
                    start_date__range=(start_date, end_date),
                    end_date__range=(start_date, end_date),
                )

                # Filter items based on paid or less than 2 hours since booking
                items = items.filter(Q(payment_status=1) | Q(create_data__range=(
                    datetime.now(start_date.tzinfo) - timedelta(hours=2), datetime.now(start_date.tzinfo))))

                # get list of all residence id that not free
                residence_reserved_id_list = items.values_list('residence_id')

                # all residence exclude not free list
                all_hotel_free_room = Residence.objects.all().exclude(
                    id__in=[item[0] for item in residence_reserved_id_list])

                # annotate some information that we need them
                all_hotel_free_room = all_hotel_free_room.annotate(
                    adult_number_difference=ExpressionWrapper(adult_num - F('standard_capacity_detail__adult_number'),
                                                              output_field=DecimalField(max_digits=10,
                                                                                        decimal_places=2)),
                    baby_number_difference=ExpressionWrapper(child_num - F('standard_capacity_detail__child_number'),
                                                             output_field=DecimalField(max_digits=10,
                                                                                       decimal_places=2)),
                    child_number_difference=ExpressionWrapper(baby_num - F('standard_capacity_detail__baby_number'),
                                                              output_field=DecimalField(max_digits=10,
                                                                                        decimal_places=2)),
                    standard_total_price=ExpressionWrapper(F('standard_capacity_detail__total_price') * interval,
                                                           output_field=DecimalField(max_digits=10,
                                                                                     decimal_places=2)),

                ).order_by('adult_number_difference', 'baby_number_difference', 'child_number_difference',
                           'standard_total_price')

                serializer = FreeResidenceSerializer(data=all_hotel_free_room, context={'interval': interval},
                                                     many=True)
                serializer.is_valid()
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(data={'error_messages': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
