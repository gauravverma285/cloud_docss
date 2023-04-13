from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import date
import threading
from rest_framework import status as tstatus
from .serializers import *
from universal.mailing import (
	signupMail,
	resetPassMail,
	resendOtpMail,
	verifyEMail
)
from universal.methods import (
	otp_func,
)


from .models import *
# from .serializers import *

class SignupApiView(APIView):
	""" API for signup """

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for signup api """
		res = {}
		try:
			email = request.POST.get("email", None)
			password = request.POST.get("password", None)
			cpassword = request.POST.get("cpassword", None)
			name = request.POST.get('name', None)
			mobile = request.POST.get('mobile', None)
			dob = request.POST.get('dob', None)

			if email is None:
				res['status'] = False
				res['message'] = "Email is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
				res['status'] = False
				res['message'] = "Account already exist with this Email"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if name is None:
				res['status'] = False
				res['message'] = "Name is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if password is None or password != cpassword:
				res['status'] = False
				res['message'] = "Password not Match!"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
			
			if mobile is None:
				res['status'] = False
				res['message'] = "Mobile_no is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
			
			if dob is None:
				res['status'] = False
				res['message'] = "Dob is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			data = request.data
			try:
				data._mutable = True
			except:
				pass
			data['username'] = email
			data['status'] = 'Active'
			
			
			serializer = UserSerializer(
				data=data, context={'request': request})
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				res_data = serializer.data
				user = User.objects.filter(id=res_data['id']).last()
				user.set_password(password)
				user.save()

				name = str(user.name)
				recipient_list = [user.email]

				otp = otp_func()
				user.otp = otp
				user.save()
				start_thread = threading.Thread(target=signupMail, args=(
					"Please verify Email to complete your Registration", recipient_list, name, otp))
				start_thread.start()
				print(otp, recipient_list, name)
			
				res['status'] = True
				res['message'] = "You've registered successfully"
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)
			else:
				res['status'] = False
				error = next(iter(serializer.errors))
				res['message'] = serializer.errors[str(error)][0]
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
		


class LoginApiView(APIView):
	""" API for login """

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for login api """
		res = {}
		try:
			username = request.POST.get("username", None)
			password = request.POST.get("password", None)

			if username is None:
				res['status'] = False
				res['message'] = "Email is required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

			if password is None:
				res['status'] = False
				res['message'] = "Password is required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

			user = authenticate(username=username, password=password)
			if user is None:
				res['status'] = False
				res['message'] = "Invalid Email or Password!"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_400_BAD_REQUEST) 
			else:
				
				serializer = UserSerializer(user, read_only=True, context={'request': request})
				if serializer :
					res['status'] = True
					res['message'] = "Authenticated successfully"
					res['data'] = serializer.data
					return Response(res, status=tstatus.HTTP_200_OK)
				else:
					res['status'] = False
					res['message'] = "Invalid Email or Password!!"
					res['data'] = []
					return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
				
		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
		
class ResetPasswordApiView(APIView):
	""" API for reset password """

	permission_classes = [IsAuthenticated]

	def post(self, request):
		""" post method for reset password API """
		res = {}
		try:
			old_password = request.POST.get('old_password', None)
			new_password = request.POST.get('new_password', None)
			re_password = request.POST.get('re_password', None)
			user = User.objects.filter(id=request.user.id).last()
			if user is None:
				res['status'] = False
				res['message'] = 'No such Authenticated User.'
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			if old_password is None:
				res['status'] = False
				res['message'] = 'Old password is required'
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			if not user.check_password(old_password):
				res['status'] = False
				res['message'] = 'Password not Match!'
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			if new_password is None:
				res['status'] = False
				res['message'] = 'New password is required'
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			if re_password is None:
				res['status'] = False
				res['message'] = 'Confirm password is required'
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			if str(new_password) != str(re_password):
				res['status'] = False
				res['message'] = 'New password and confirm password not match.'
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			else:
				user.set_password(new_password)
				user.save()
				try:
					user.auth_token.delete()
				except:
					pass
				new_user = authenticate(
					username=user.username, password=new_password)
				if new_user:
					serializer = UserSerializer(new_user, read_only=True)
					res['status'] = True
					res['message'] = 'Password reset successfully.'
					res['data'] = serializer.data
					return Response(res, status=tstatus.HTTP_200_OK)

				else:
					res['status'] = False
					res['message'] = 'Password reset but unable to authenticate user, please try again.'
					res['data'] = []
					return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)


class ForgotPasswordApiView(APIView):
	"""forgot password API view"""

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for forgot password API """

		res = {}
		try:
			email = request.data.get('email', None)
			if email is None:
				res['status'] = False
				res['message'] = "Email is required."
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			user = User.objects.filter(username=email).last()
			if user is None:
				res['status'] = False
				res['message'] = "No such user registered with this email."
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			else:
				user.otp = otp_func()
				user.save()
				name = user.name
				subject = "Here is your OTP to Reset Password"
				recipient_list = [user.email]
				otp = user.otp
				resetPassMail(subject, recipient_list, name, otp)
				res['status'] = True
				res['message'] = "Otp sent Successfully"
				res['data'] = {'id': user.id}
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)


#API for Add client

class AddClientApiView(APIView):
	""" API for Add client """

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for AddClient api """
		res = {}
		try:
			email = request.POST.get("email", None)
			name = request.POST.get('name', None)
			mobile = request.POST.get('mobile', None)
			
			if email is None:
				res['status'] = False
				res['message'] = "Email is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if Client.objects.filter(email=email).exists():
				res['status'] = False
				res['message'] = "Account already exist with this Email"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if name is None:
				res['status'] = False
				res['message'] = "Name is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
			
			if mobile is None:
				res['status'] = False
				res['message'] = "Mobile_no is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
			
			data = request.data
			try:
				data._mutable = True
			except:
				pass
			# data['username'] = email
			
			
			serializer = ClientSerializer(
				data=data, context={'request': request})
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				res_data = serializer.data
				res['status'] = True
				res['message'] = "You've Added successfully"
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)
			else:
				res['status'] = False
				error = next(iter(serializer.errors))
				res['message'] = serializer.errors[str(error)][0]
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

class GetClientAPiView(APIView):
	""" API for get Client detail """

	permission_classes = [IsAuthenticated]

	def get(self, request):
		""" get method for get Client detail API """

		res = {}
		try:
			# client_id = request.GET.get('client', None)
			
			client = Client.objects.all()
			
			if client is None:
				res['status'] = False
				res['message'] = "Client not found."
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			serializer = ClientSerializer(
				client, read_only=True, many=True, context={'request': request})
			if serializer:
				res['status'] = True
				res['message'] = 'Client detail fetched successfully'
				res['data'] = serializer.data
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)




#API for Particular Client

class ParticularClientApiView(APIView):
	""" API for Particular client """

	permission_classes = [IsAuthenticated]

	def post(self, request):
		""" post method for Particular api """
		res = {}
		try:
			email = request.POST.get("email", None)
			name = request.POST.get('name', None)
			mobile = request.POST.get('mobile', None)
			# client_id = request.POST.get('client', None)
			
			if email is None:
				res['status'] = False
				res['message'] = "Email is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if Client.objects.filter(email=email).exists():
				res['status'] = False
				res['message'] = "Account already exist with this Email"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

			if name is None:
				res['status'] = False
				res['message'] = "Name is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
			
			if mobile is None:
				res['status'] = False
				res['message'] = "Mobile_no is Required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
			
			data = request.data
			try:
				data._mutable = True
			except:
				pass
			# data['username'] = email
			
			
			serializer = ClientSerializer(
				data=data, context={'request': request})
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				res_data = serializer.data
				res['status'] = True
				res['message'] = "You've Added successfully"
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)
			else:
				res['status'] = False
				error = next(iter(serializer.errors))
				res['message'] = serializer.errors[str(error)][0]
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)



class ClientDocumentApiView(APIView):
	""" API for Add client document """

	permission_classes = [IsAuthenticated]

	def post(self, request):
		res = {}
		try:
			client = None
			client_id = request.GET.get("client", None)
			document = request.data.get("document", None)
			print(client_id, document)

			if client_id is None:
				res['status'] = False
				res['message'] = "Client_id not found."
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)
			
			client = Client.objects.filter(id=client_id).last()
			if client is None:
				res['status'] = False
				res['message'] = "Client not Found"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
		
			if document is None:
				res['status'] = False
				res['message'] = "Document is required"
				res['data'] = []
				return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
			
			data = request.data
			try:
				data._mutable = True
			except:
				pass
			data['client'] = client.id
		
			serializer = ClientDocumentSerializer(data=data, context={'request': request})
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				res_data = serializer.data
				res['status'] = True
				res['message'] = "Your Document Added successfully"
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)
			else:
				res['status'] = False
				error = next(iter(serializer.errors))
				res['message'] = serializer.errors[str(error)][0]
				res['data'] = res_data
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
		


class GetDocumentAPiView(APIView):
	""" API for get Client document """

	permission_classes = [IsAuthenticated]

	def get(self, request):
		""" get method for get Client document API """

		res = {}
		try:
			client_id= request.GET.get('client', None)
			client = Client.objects.filter(id=client_id).last()
			document = ClientDocument.objects.filter(client=client).all()
			# client = ClientDocument.objects.all()
			
			if client is None:
				res['status'] = False
				res['message'] = "Client not found."
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			serializer = ClientDocumentSerializer(
				document, read_only=True, many=True, context={'request': request})
			if serializer:
				res['status'] = True
				res['message'] = 'Client detail fetched successfully'
				res['data'] = serializer.data
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
		


class ForgotPasswordApiView(APIView):
	"""forgot password API view"""

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for forgot password API """

		res = {}
		try:
			email = request.data.get('email', None)
			if email is None:
				res['status'] = False
				res['message'] = "Email is required."
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			user = User.objects.filter(username=email).last()
			if user is None:
				res['status'] = False
				res['message'] = "No such user registered with this email."
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			else:
				user.otp = otp_func()
				user.save()
				name = user.name
				subject = "Here is your OTP to Reset Password"
				recipient_list = [user.email]
				otp = user.otp
				resetPassMail(subject, recipient_list, name, otp)
				res['status'] = True
				res['message'] = "Otp sent Successfully"
				res['data'] = {'id': user.id}
				return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)


class VerifyEmailApiView(APIView):
	""" API for verify email address """

	permission_classes = [IsAuthenticated]

	def post(self, request):
		res = {}
		try:
			user_id = request.data.get('user_id', None)
			otp = request.data.get('otp', None)

			if user_id is None:
				res['status'] = False
				res['message'] = 'User id is required'
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			user = User.objects.filter(id=user_id).last()
			if user is None:
				res['status'] = False
				res['message'] = 'No user exist with given user id'
				res['data'] = []
				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

			if otp:
				if str(user.otp) == str(otp):
					user.is_verified = True
					user.otp = otp_func()
					user.save()

					res['status'] = True
					res['message'] = "User Verified successfully."
					res['data'] = []
					return Response(res, status=tstatus.HTTP_200_OK)

				else:
					res['status'] = False
					res['message'] = 'OTP is not valid.'
					res['data'] = []
					return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)
			# else:
			# 	name = str(user.name)
			# 	subject = "Your Email verified Successfully!"
			# 	recipient_list = [user.email]
			# 	otp = otp_func()
			# 	user.otp = otp
			# 	user.save()
			# 	verifyEMail(subject, recipient_list, name, otp)

			# 	res['status'] = True
			# 	res['message'] = "An OTP sent to your email ID."
			# 	res['data'] = []
			# 	return Response(res, status=tstatus.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
		



class ForgotResetPasswordApiView(APIView):
	"""forgot reset password API view"""

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for reset password API """

		res = {}
		try:
			otp = request.data.get('otp', None)
			user_id = request.data.get('user_id', None)
			password = request.data.get('password', None)
			re_password = request.data.get('re_password', None)
			if otp:
				if user_id is None:
					res['status'] = False
					res['message'] = "User's ID is required."
					res['data'] = []
					return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

				user = User.objects.filter(id=user_id).last()
				if user is None:
					res['status'] = False
					res['message'] = "No such user register with this ID."
					res['data'] = []
					return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

				if str(user.otp) == str(otp):
					res['status'] = True
					res['message'] = 'Otp verified successfully, Now you can reset password.'
					res['data'] = {'id': user.id}
					return Response(res, status=tstatus.HTTP_200_OK)

				else:
					res['status'] = False
					res['message'] = 'Otp are not valid.'
					res['data'] = []
					return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

			else:
				if password and re_password and str(password) == str(re_password):
					if user_id is None:
						res['status'] = False
						res['message'] = "User's ID is required."
						res['data'] = []
						return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

					user = User.objects.filter(id=user_id).last()
					if user is None:
						res['status'] = False
						res['message'] = "No such user registered with this ID."
						res['data'] = []
						return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

					else:
						user.set_password(password)
						user.otp = None
						user.save()
						res['status'] = True
						res['message'] = 'Password changes successfully.'
						res['data'] = []
						return Response(res, status=tstatus.HTTP_200_OK)
				else:
					res['status'] = False
					res['message'] = 'Password not Match!'
					res['data'] = []
					return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)


class EditClientApiView(APIView):
	""" API for edit user client """

	permission_classes = [IsAuthenticated]

	def post(self, request, id=None):
		""" post method for edit client API """

		res = {}
		# try:
		# client = id
		# client_id= request.GET.get('client', None)
		# client = Client.objects.filter(id=client_id).last()
		is_delete = request.data.get('is_delete', None)
		name = request.data.get('name', None)
		email = request.data.get('email', None)
		mobile = request.data.get('mobile', None)

		client = Client.objects.filter(id=id, status='Active').last()
		if client is None:
			res['status'] = False
			res['message'] = "client not found."
			res['data'] = []
			return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)


		if is_delete:
		
			# client = Client.objects.filter(id=id).last()

			
			client.status="Delete"
			client.save

			res['status'] = True
			res['message'] = "Profile Deleted Successfully,"
			res['data'] = []
			return Response(res, status=tstatus.HTTP_200_OK)

		else:

			# if client is None:
			# 	res['status'] = False
			# 	res['message'] = "client not found."
			# 	res['data'] = []
			# 	return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

		# if str(client.name) == name:
		# 	if Client.objects.filter(name=name, status='Active').exists():
		# 		res['status'] = False
		# 		res['message'] = "name already exists"
		# 		res['data'] = []
		# 		return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

		# if str(client.email) == email:
		# 	if Client.objects.filter(email=email, status='Active').exists():
		# 		res['status'] = False
		# 		res['message'] = "Email already exists"
		# 		res['data'] = []
		# 		return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)
			
		# if str(client.mobile) == mobile:
		# 	if Client.objects.filter(mobile=mobile, status='Active').exists():
		# 		res['status'] = False
		# 		res['message'] = "mobile already exists"
		# 		res['data'] = []
		# 		return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)


			client_obj = client
			data = request.data
		try:	
			data._mutable = True
		except:
			pass
		
		if email and client.email != email:
			data['email'] = email
			data['email_verified'] = False
			data['username'] = email

			serializer = ClientSerializer(data=data, instance=client_obj)

			if serializer.is_valid(raise_exception=True):
				serializer.save()
				res['status'] = True
				res['message'] = "Profile updated Successfully, please verify email first."
				res['data'] = serializer.data
				return Response(res, status=tstatus.HTTP_200_OK)

			else:
				res['status'] = False
				error = next(iter(serializer.errors))
				res['message'] = serializer.errors[str(error)][0]
				res['data'] = []
				return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

		else:
			data['email'] = client.email
			data['username'] = client.email
			data['email_verified'] = True

			serializer = ClientSerializer(
				data=data, instance=client_obj, context={'request': request})
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				res['status'] = True
				res['message'] = "Profile updated Successfully"
				res['data'] = serializer.data
				return Response(res, status=tstatus.HTTP_200_OK)

			else:
				res['status'] = False
				error = next(iter(serializer.errors))
				res['message'] = serializer.errors[str(error)][0]
				res['data'] = []
				return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
	
		# except Exception as e:
		# 	res['status'] = False
		# 	res['message'] = str(e)
		# 	res['data'] = []
		# 	return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

















# class ForgotPasswordApiView(APIView):
# 	"""forgot password API view"""

# 	permission_classes = [AllowAny]

# 	def post(self, request):
# 		""" post method for forgot password API """

# 		res = {}
# 		try:
# 			email = request.data.get('email', None)
# 			if email is None:00000000
# 				res['status'] = False
# 				res['message'] = "Email is required."
# 				res['data'] = []
# 				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

# 			user = User.objects.filter(username=email, role__in=[
# 									   'User', 'Student'], status="Active").last()
# 			if user is None:
# 				res['status'] = False
# 				res['message'] = "No such user registered with this email."
# 				res['data'] = []
# 				return Response(res,  status=tstatus.HTTP_404_NOT_FOUND)

# 			else:
# 				user.otp = otp_func()
# 				user.save()
# 				name = user.name
# 				subject = "Here is your OTP to Reset Password"
# 				recipient_list = [user.email]
# 				otp = user.otp
# 				resetPassMail(subject, recipient_list, name, otp)
# 				res['status'] = True
# 				res['message'] = "Otp sent Successfully"
# 				res['data'] = {'id': user.id}
# 				return Response(res, status=tstatus.HTTP_200_OK)

# 		except Exception as e:
# 			res['status'] = False
# 			res['message'] = str(e)
# 			res['data'] = []
# 			return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

	 

		



# @login_required(login_url='home:login')
# def profile(request):
# 	user = User.objects.filter(id=request.user.id).first()
# 	form = UserProfileForm(instance=user)
# 	if request.method == "POST":
# 		form = UserProfileForm(request.POST,request.FILES,instance=user)
# 		request.POST._mutable = True
# 		if form.is_valid():
# 			user_obj = form.save(commit=False)
# 			user_obj.username = request.user.username
# 			user_obj.save()
# 			messages.success(request,"Profile Updated")
# 			return redirect('home:profile')
# 		else:
# 			messages.error(request, "invalid")
# 	return render(request, 'common/profile.html', {'form':form,'user':user})

