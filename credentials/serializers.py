from rest_framework import serializers
from credentials.models import Credential
from utils.encryption import encrypt_password, decrypt_password


class CredentialSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    decrypted_password = serializers.SerializerMethodField()

    class Meta:
        model = Credential
        fields = [
            'id', 
            'category', 
            'site_name', 
            'username', 
            'email', 
            'phone_number',
            'site_url', 
            'other', 
            'password', 
            'decrypted_password',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'decrypted_password']

    def get_decrypted_password(self, obj):
        user = self.context['request'].user
        return decrypt_password(user, obj.password_encrypted)

    def create(self, validated_data):
        user = self.context['request'].user
        plain_password = validated_data.pop('password')
        validated_data['password_encrypted'] = encrypt_password(user, plain_password)
        return Credential.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if 'password' in validated_data:
            plain_password = validated_data.pop('password')
            instance.password_encrypted = encrypt_password(user, plain_password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
