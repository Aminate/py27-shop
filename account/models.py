from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .tasks import send_activation_code

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
        send_activation_code.delay(user.email, user.create_activation_code)
        user.save(using=self._db)  #это мы сохраняем юзера в бд
        Billing.objects.create(user=user)
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


class Billing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='billing')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def top_up(self, amount):
        "пополнение счета,если транзакция прошла успещна вернется True"
        if amount > 0:
            self.amount += amount
            self.save()
            return True
        return False

    def withdraw(self, amount):
        "снятие денег со счета"
        if self.amount >= amount:
            self.amount -= amount
            self.save()
            return True
        return False


