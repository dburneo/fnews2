from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User   # Esta línea es para el Profile
from django.utils import timezone   # Probar a ver si funciona sin esta línea
from django.utils.translation import gettext_lazy as _  # Probar a ver si funciona sin esta línea
from django.conf import Settings

# from django.db.models.signals import post_save
# from django.dispatch import receiver

import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, first_name, last_name, password=None,commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(_('first name'), max_length=60, blank=True)
    last_name = models.CharField(_('last name'), max_length=60, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         User.objects.create_user(user=instance)
#     instance.user.save()
