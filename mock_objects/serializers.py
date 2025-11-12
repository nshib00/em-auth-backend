from rest_framework.serializers import Serializer, IntegerField, CharField


class MockOrderSerializer(Serializer):
    id = IntegerField()
    title = CharField(required=False)
    amount = CharField(required=False)


class MockProductSerializer(Serializer):
    id = IntegerField()
    title = CharField(required=False)
    amount = CharField(required=False)
