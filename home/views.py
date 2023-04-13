# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login




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

# def Login(request):
# 	if request.method == 'POST':
# 		email = request.POST.get('email', None)
# 		password = request.POST.get('password', None)
# 		if email and password:
# 			user = authenticate(username=email, password=password)
		
# 	return render(request, 'common/login.html', {})