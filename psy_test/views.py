from rest_framework import serializers, generics

from psy_test.models import Test, TestOption


class TestOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestOption
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    options = TestOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = '__all__'


class TestList(generics.ListAPIView):
    pagination_class = None
    serializer_class = TestSerializer
    queryset = Test.objects.all()
