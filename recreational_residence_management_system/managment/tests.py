from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APITestCase
from managment.models import Residence, StandardCapacityDetail, ExtraCapacityDetail
from managment.serializers import ResidenceSerializer, StandardCapacityDetailSerializer, ExtraCapacityDetailSerializer


# Define the test class for the serializers
class SerializerTestCase(APITestCase):
    # A test class for the serializers that inherits from APITestCase

    def setUp(self):
        # A method to set up some sample data for testing
        # Create a residence instance
        self.residence = Residence.objects.create(name="Residence A", description="A cozy and comfortable residence")
        # Create some standard capacity detail instances
        self.standard_capacity_detail_1 = StandardCapacityDetail.objects.create(
            residence=self.residence,
            adult_number=2,
            child_number=1,
            baby_number=0,
            adult_price=100.00,
            child_price=50.00,
            baby_price=0.00
        )
        self.standard_capacity_detail_2 = StandardCapacityDetail.objects.create(
            residence=self.residence,
            adult_number=4,
            child_number=2,
            baby_number=1,
            adult_price=150.00,
            child_price=75.00,
            baby_price=25.00
        )
        # Create an extra capacity detail instance
        self.extra_capacity_detail = ExtraCapacityDetail.objects.create(
            residence=self.residence,
            extra_adult_price=50.00,
            extra_child_price=25.00,
            extra_baby_price=10.00
        )
        # Create a serializer instance for the residence with the nested serializers
        self.serializer = ResidenceSerializer(self.residence)

    def test_serializer_data(self):
        # A method to test the serializer data against the expected data
        # Define the expected data as a dictionary
        expected_data = {
            "name": "Residence A",
            "description": "A cozy and comfortable residence",
            "standard_capacity_detail": [
                {
                    "id": self.standard_capacity_detail_1.id,
                    "residence": self.residence.id,
                    "adult_number": 2,
                    "child_number": 1,
                    "baby_number": 0,
                    "adult_price": "100.00",
                    "child_price": "50.00",
                    "baby_price": "0.00",
                    "standard_capacity": 3,
                    "total_price": "200.00"
                },
                {
                    "id": self.standard_capacity_detail_2.id,
                    "residence": self.residence.id,
                    "adult_number": 4,
                    "child_number": 2,
                    "baby_number": 1,
                    "adult_price": "150.00",
                    "child_price": "75.00",
                    "baby_price": "25.00",
                    "standard_capacity": 7,
                    "total_price": "725.00"
                }
            ],
            "extra_capacity_detail": [
                {
                    "id": self.extra_capacity_detail.id,
                    "residence": self.residence.id,
                    "extra_adult_price": "50.00",
                    "extra_child_price": "25.00",
                    "extra_baby_price": "10.00"
                }
            ]
        }
        # Assert that the serializer data is equal to the expected data
        self.assertEqual(self.serializer.data, expected_data)
