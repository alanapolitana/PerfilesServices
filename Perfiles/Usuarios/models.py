""" from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group 

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, role, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True) 
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, default='',blank=False, null=True) 
    first_name = models.CharField(max_length=30,default='', blank=False)
    last_name = models.CharField(max_length=30,default='', blank=False)
    address = models.CharField(max_length=255, default='', blank=False)
    phone = models.CharField(max_length=20, default='', blank=False)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, default=1, related_name='users')

    # Cambiar los nombres de las relaciones inversas para evitar el conflicto con el modelo auth.User
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'


class Role(models.Model):
    id_role = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name
 """
 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.forms import ValidationError
from django.utils.timezone import now
from django.utils import timezone


# --- Manager personalizado para el modelo User ---
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, role, **extra_fields)


# --- Modelo User ---
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, default='', blank=False, null=True)
    first_name = models.CharField(max_length=30, default='', blank=False)
    last_name = models.CharField(max_length=30, default='', blank=False)
    address = models.CharField(max_length=255, default='', blank=False)
    phone = models.CharField(max_length=20, default='', blank=False)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, default=1, related_name='users')

    # Cambiar nombres de relaciones inversas
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'


# --- Modelo Role ---
class Role(models.Model):
    id_role = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name

def validate_positive(value):
    """Validator to ensure the value is positive."""
    if value <= 0:
        raise ValidationError('The value must be positive.')
    
class BMI(models.Model):  # BMI (Body Mass Index)
    id_bmi = models.AutoField(primary_key=True)  # Primary key
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bmi_records')  # Relationship with User
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_positive])  # Weight in kg
    height = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_positive])  # Height in meters
    date = models.DateTimeField(default=now)  # Record date date = models.DateTimeField(default=timezone.now)


    class Meta:
        db_table = 'bmi'
        verbose_name = 'BMI'
        verbose_name_plural = 'BMIs'

    def __str__(self):
        return f"BMI of {self.user.email} - {self.date.strftime('%Y-%m-%d')}"

    @property
    def bmi(self):
        """Calculates BMI as a property."""
        if self.height > 0:
            return round(self.weight / (self.height ** 2), 2)
        return None