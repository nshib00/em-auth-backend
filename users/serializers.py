from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, validators=[validate_password])
    password_confirm = CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise ValidationError({"password_confirm": "Passwords don't match"})
        attrs.pop('password_confirm')  # далее поле подтверждения пароля не будет нужно
        return attrs

    def create(self, validated_data):
        User = get_user_model()
        password = validated_data.pop('password')
        
        try:
            user = User.objects.create_user(
                password=password,
                **validated_data
            )
            return user
        except Exception as e:
            raise ValidationError({'Error while creating user': str(e)})