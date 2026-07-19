from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "password",
        ]
        read_only_fields = [
            "id",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": False,
                "min_length": 8,
            },
        }

    def validate(self, attrs):
        if (
            self.instance is None
            and not attrs.get("password")
        ):
            raise serializers.ValidationError(
                {
                    "password": (
                        "A senha é obrigatória para "
                        "criar um usuário."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop(
            "password",
            None,
        )

        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance