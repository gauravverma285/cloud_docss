from email.headerregistry import Address
import math, random
import string
from django.conf import settings
 
# function to generate OTP
def otp_func() :
 
	# Declare a digits variable 
	# which stores all digits
	digits = "0123456789"
	OTP = ""
 
   # length of password can be changed
   # by changing value in range
	for i in range(6) :
		OTP += digits[math.floor(random.random() * 10)]
 
	return OTP
