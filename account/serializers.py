from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

class UserRegisterSLR(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'password2', 'tc')
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs.get('password2'):
            raise serializers.ValidationError("Password Does't Match !")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class UserLoginSLR(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    class Meta:
        model = User
        fields = ('email', 'password')

class UserProfileSLR(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'created_at')

class UserChangePasswordSLR(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ('password', 'password2')
    
    def validate(self, attrs):
        password = attrs['password']
        user = self.context.get('user')
        if password != attrs['password2']:
            raise serializers.ValidationError("Password Does't match")
        user.set_password(password)
        user.save()
        return attrs

class SendEmailResetPasswordSLR(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    class Meta:
        fields = ('email',)
    
    def validate(self, attrs):
        if not User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Please Provide Valid Email!')
        else:
            user = User.objects.get(email=attrs['email'])
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/rpv/'+uid+'/'+token+'/'
            print('Link', link)
            # Send Email
            data = {
                'subject':'Reset Your Password',
                'message':f'Click follow link to reset your password ---> {link}',
                'to_email':(user.email,)
            }
            Util.send_link(data)
            return attrs

class ResetPasswordSLR(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ('password', 'password2')
    
    def validate(self, attrs):
        password = attrs['password']
        user = User.objects.get(id=smart_str(urlsafe_base64_decode(self.context['uid'])))
        if PasswordResetTokenGenerator().check_token(user, self.context['token']):
            if password != attrs['password2']:
                raise serializers.ValidationError("Password Does't match")
            user.set_password(password)
            user.save()
            return attrs
        else:
            raise serializers.ValidationError("Token has been Expire or Does't Valid")
