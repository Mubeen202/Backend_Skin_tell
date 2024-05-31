from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import *
import datetime
from .utils import validate_email as email_is_valid
from json import JSONEncoder
from uuid import UUID
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
old_default = JSONEncoder.default

class RegistrationSerializer(serializers.ModelSerializer[User]):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(max_length=128, min_length=8)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'bio',
            'full_name',
            'is_active',
            'is_simpleuser', 
            'is_superuser', 
            'user_created_by',
            'created_at',
            'updated_at'
        ]

    def validate_email(self, value: str) -> str:
        """Normalize and validate email address."""
        valid, error_text = email_is_valid(value)
        if not valid:
            raise serializers.ValidationError(error_text)
        try:
            email_name, domain_part = value.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            value = '@'.join([email_name, domain_part.lower()])

        return value

    def create(self, validated_data):  # type: ignore
        """Return user after creation."""
        # Extract is_simpleuser and is_superuser from validated_data
        is_simpleuser = validated_data.pop('is_simpleuser', False)
        is_superuser = validated_data.pop('is_superuser', False)
        
        # Create the user with the extracted data
        user = User.objects.create_user(
            username=validated_data['username'],  
            full_name=validated_data['full_name'], 
            email=validated_data['email'], 
            password=validated_data['password'],
        )
        user.bio = validated_data.get('bio', '')
        user.is_simpleuser = is_simpleuser  # Set the is_simpleuser attribute
        user.is_superuser = is_superuser    # Set the is_superuser attribute
        user.save(update_fields=['bio', 'is_simpleuser', 'is_superuser'])
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True)  # Exclude password from response


    class Meta:
        model = User
        fields = '__all__'
        # read_only_fields = ('user_created_by',)  # Make 'id' field read-only

    # def create(self, validated_data):
    #     # Extract password from validated data
    #     # Extract is_simpleuser and is_superuser from validated_data
    #     is_simpleuser = validated_data.pop('is_simpleuser', False)
    #     is_superuser = validated_data.pop('is_superuser', False)
    #     user_created_by = validated_data.pop('user_created_by', '')
        
    #     # Create the user with the extracted data
    #     user = User.objects.create_user(
    #         username=validated_data['username'],  
    #         full_name=validated_data['full_name'], 
    #         email=validated_data['email'], 
    #         password=validated_data['password'],
    #     )
    #     user.bio = validated_data.get('bio', '')
    #     user.is_simpleuser = is_simpleuser  # Set the is_simpleuser attribute
    #     user.is_superuser = is_superuser    # Set the is_superuser attribute
    #     user.user_created_by = user_created_by    # Set the is_superuser attribute
    #     user.save(update_fields=['bio', 'is_simpleuser', 'is_superuser', 'user_created_by'])
    #     return user

    def create(self, validated_data):
        # Extract password from validated data
        password = validated_data.pop('password')
        # Create user instance with hashed password
        is_simpleuser = validated_data.pop('is_simpleuser', False)
        user = User.objects.create_user(password=password, **validated_data)
        user.is_simpleuser = is_simpleuser
        user.save(update_fields=['bio', 'is_simpleuser'])
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert UUID to string for user_created_by field
        representation['user_created_by'] = str(representation['user_created_by'])
        return representation


class LoginSerializer(serializers.ModelSerializer[User]):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):  # type: ignore
        """Get user token."""
        user = User.objects.get(email=obj.email)

        return {'refresh': user.tokens['refresh'], 'access': user.tokens['access']}

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'tokens', 'full_name', 'is_staff', 'is_superuser', 'is_simpleuser']

    def validate(self, data):  # type: ignore
        """Validate and return user login."""
        email = data.get('email', None)
        password = data.get('password', None)
        users = User.objects.filter(email=email).first()
        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if users is None:
            raise serializers.ValidationError('Username doesn’t exist. Contact administrator.')
        
        if not users.check_password(password):
            raise serializers.ValidationError('Password is incorrect.')
        if not user.is_active:
            raise serializers.ValidationError('This user is not currently activated.')
        return user

 
class UserSerializer(serializers.ModelSerializer[User]):
    """Handle serialization and deserialization of User objects."""
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'tokens',
            'bio',
            'full_name',
            'birth_date',
            'is_staff',
            'groups',
            'is_superuser',
            'is_simpleuser'
            
        )
        read_only_fields = ('tokens', 'is_staff')

    def update(self, instance, validated_data):  # type: ignore
        """Perform an update on a User."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
    
    
    


class LogoutSerializer(serializers.Serializer[User]):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type: ignore
        """Validate token."""
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):  # type: ignore
        """Validate save backlisted token."""

        try:
            RefreshToken(self.token).blacklist()

        except TokenError as ex:
            raise exceptions.AuthenticationFailed(ex)


class GettingUserRegistrationSerializer(serializers.ModelSerializer[User]):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(max_length=128, min_length=8)
    # usersRoles = GettingUserRolesSerializer(many=True, read_only=True)
  

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'tokens',
            'bio',
            'full_name',
            'birth_date',
            'is_staff',
            'full_name',
            # 'usersRoles',
            'is_superuser',
            'is_simpleuser'
        ]

    def validate_email(self, value: str) -> str:
        """Normalize and validate email address."""
        valid, error_text = email_is_valid(value)
        if not valid:
            raise serializers.ValidationError(error_text)
        try:
            email_name, domain_part = value.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            value = '@'.join([email_name, domain_part.lower()])

        return value

    def create(self, validated_data):  # type: ignore
            """Return user after creation."""
            user = User.objects.create_user(
                username=validated_data['username'], full_name=validated_data['full_name'], email=validated_data['email'], password=validated_data['password'],
            )
            user.bio = validated_data.get('bio', '')
            # user.full_name = validated_data.get('full_name', '')
            user.save(update_fields=['bio'])
            return user
    # def create(self, validated_data):
        
    #     usersRoles = validated_data.pop('usersRoles')
    #     userId = User.objects.create(**validated_data)
    #     def new_default(self, obj):
    #         if isinstance(obj, UUID):
    #             return str(obj)
    #         return old_default(self, obj)
    #     JSONEncoder.default = new_default
    #     for role in usersRoles:
    #         UserRoles.objects.create(**role, userId=userId)
    #     return userId
    
    