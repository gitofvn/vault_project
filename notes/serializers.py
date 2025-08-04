# notes/serializers.py
from rest_framework import serializers
from notes.models import Note
from utils.encryption import encrypt_password, decrypt_password

class NoteSerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)      
    decrypted_content = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'decrypted_content', 'created_at', 'updated_at']

    def get_decrypted_content(self, obj):
        user = self.context['request'].user
        return decrypt_password(user, obj.content)

    def create(self, validated_data):
        user = self.context['request'].user
        plaintext_content = validated_data.pop('content')
        validated_data['content'] = encrypt_password(user, plaintext_content)
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if 'content' in validated_data:
            plaintext_content = validated_data.pop('content')
            validated_data['content'] = encrypt_password(user, plaintext_content)
        return super().update(instance, validated_data)
