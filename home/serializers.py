from rest_framework import serializers
from rest_framework.authtoken.models import Token
from universal.mailing import signupMail
from universal.methods import otp_func
from .models import *



class UserSerializer(serializers.ModelSerializer):
	""" user serializer """

	token_detail = serializers.SerializerMethodField("get_token_detail")
	class Meta:
		model = User 
		fields = ('id', 'username', 'name', 'email', 'mobile','dob', 'token_detail', 'is_verified')
		extra_kwargs = {
			'token_detail': {'read_only': True}
		}
		
	def get_token_detail(self, obj):
		token, created = Token.objects.get_or_create(user=obj)
		return token.key

	def get_user(self, request):
		user = request
		return user 
	

class ClientSerializer(serializers.ModelSerializer):

	class Meta:
		model = Client
		fields = ('name', 'email', 'mobile','id')

	def get_client(self, request):
		client = request
		return client 
	


class ClientDocumentSerializer(serializers.ModelSerializer):

		class Meta:
			model = ClientDocument
			fields = ('client','document')

		def get_clientdocument(self, request):
			clientdocument = request
			return clientdocument 
	
	
		

	



	