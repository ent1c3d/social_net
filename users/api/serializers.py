import logging
from requests import HTTPError

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
import clearbit
from pyhunter import PyHunter

from social_net.settings import CLEARBIT_API_KEY, EMAILHUNTER_API_KEY, \
    USE_CLEARBIT, USE_EMAILHUNTER

clearbit.key = CLEARBIT_API_KEY
hunter = PyHunter(EMAILHUNTER_API_KEY)

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {"password":{"write_only": True}}

    def validate(self, data):
        email = data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError("The user with the following email is already registered.")
        if USE_CLEARBIT:
            if not all([data.get('first_name'), data.get('last_name')]):
                try:
                    response = clearbit.Enrichment.find(email=email, stream=True)
                    if response and response['person']:
                        data['first_name'] = data['first_name'] or \
                                             response['person'].get('name').get('givenName')
                        data['last_name'] = data['last_name'] or \
                                            response['person'].get('name').get('familyName')
                except HTTPError as e:
                    logging.info(f"Can't get info for email: {email}, exception - {e}")

        return data

    def validate_email(self, value):
        email = value
        if USE_EMAILHUNTER:
            result = hunter.email_verifier(email)
            if result['result'] == 'undeliverable':
                logging.error(f"Can not verify existence of email {email}")
                raise ValidationError("Can not verify existence of email.")

        return value


    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data['password']
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user_obj = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data
