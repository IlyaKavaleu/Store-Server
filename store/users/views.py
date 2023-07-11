from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView

from products.models import Basket
from .models import User, EmailVerification
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from common.views import TitleMixin
from django.contrib.messages.views import SuccessMessageMixin

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form': UserLoginForm()}
#     return render(request, 'users/login.html', context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы'
    title = 'Store - Registration'


class UserProfileView(TitleMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Congratulations you have successfully registered!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {'form': form}
#     return render(request, 'users/register.html', context)
#

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     #for products         ----------------------WRITE TOMMOROW VIEWS FOR ALL_PRICE AND ALL_COUNT
#     price_all_products = 0
#     baskets = Basket.objects.filter(user=request.user)
#
#     # price_all_products = sum([basket.sum() for basket in baskets])
#     # sum_all_products = len([basket for basket in baskets])
#
#     context = {
#         'title': 'Store - Profile',
#         'form': form,
#         'baskets': baskets,
#         # 'price_all_products': price_all_products,
#         # 'sum_all_products': sum_all_products,
#          }
#     return render(request, 'users/profile.html', context)

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('products:index'))