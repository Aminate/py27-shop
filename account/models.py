from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .utils import send_activation_code

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **kwargs)
        #self.model = класс User
        user.set_password(password)
        user.create_activation_code()#это у нас хеширование пароля
        send_activation_code(user.email, user.create_activation_code)
        user.save(using=self._db)  #это мы сохраняем юзера в бд
        return user

    def create_superuser(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError("Email is required")
        kwargs["is_staff"] = True #даем права супер админа
        kwargs["is_superuser"] = True
        kwargs["is_active"] = True
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **kwargs)
        # self.model = класс User
        user.set_password(password)  # это у нас хеширование пароля
        user.save(using=self._db)  # это мы сохраняем юзера в бд
        return user




class User(AbstractUser):
    username = None # из полей убираем юзернайм
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    bio = models.TextField()
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)

    USERNAME_FIELD = 'email' #указываем какое поле использовать при логине
    REQUIRED_FIELDS = ['phone']

    objects = UserManager() #указываем нового менеджера


    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=10)
        self.activation_code = code
        self.save()