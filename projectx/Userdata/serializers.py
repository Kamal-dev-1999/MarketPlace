from rest_framework import serializers
from .models import MyUser, UserProfile

# Serializer for MyUser model
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    # Hash the password before saving
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# Serializer for UserProfile model
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all(), write_only=True)  # Expect PK for user

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'email', 'full_name', 'dob', 'address', 'contact_number', 'profile_img', 'bio']

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile




    
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def validate_email(self, value):
        # Add any validation logic if necessary, e.g., checking if the email exists
        return value