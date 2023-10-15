from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

    
class ManthanoUserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_superuser=is_superuser, is_active=is_active, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
    
        user.is_active=True
        user.save(using=self._db)
        return user

class ManthanoUser(AbstractUser):
    username = models.CharField('Username', max_length=32)
    first_name = models.CharField('First name', max_length=32)
    last_name = models.CharField('Last name', max_length=255)
    email = models.EmailField('Email address', max_length=255, unique=True)
    is_admin = models.BooleanField('Admin status', default=False)
    is_active = models.BooleanField('Active', default=True)
    date_joined = models.DateTimeField('Date joined', auto_now_add=True)

    # classroom = models.ForeignKey('classrooms.Classroom', on_delete=models.CASCADE, related_name='classrooms', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = ManthanoUserManager()

    class Meta:
        verbose_name = 'username'
        verbose_name_plural = 'usernames'

    def get_full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()
    
    def get_short_name(self):
        return self.first_name
    
class Profile(models.Model):
    user = models.OneToOneField("authentication.ManthanoUser", on_delete=models.CASCADE)

    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_images/')
    profile_background = models.ImageField(default='default.jpg', upload_to='profile_backgrounds/')

    desc = models.TextField('Description', null=True, blank=True)

    def __str__(self):
        return self.user.username