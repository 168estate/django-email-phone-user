""" EmailPhoneUser models."""
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class EmailPhoneUserManager(BaseUserManager):

    """ Custom Manager for EmailPhoneUser.

    For Examples check Django code:
    https://github.com/django/django/blob/master/django/contrib/auth/models.py

    """
    def normalize_phone(self, phone, country_code=None):
        phone = phone.strip().lower()
        try:
            import phonenumbers
            phone_number = phonenumbers.parse(phone, country_code)
            phone = phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.E164)
        except ImportError:
            pass

        return phone

    def _create_user(self, email_or_phone, password,
                     is_staff, is_superuser, **extra_fields):
        """ Create EmailPhoneUser with the given email or phone and password.

        :param str email_or_phone: user email or phone
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not

        :return settings.AUTH_USER_MODEL user: user
        :raise ValueError: email or phone is not set
        :raise NumberParseException: phone does not have correct format

        """
        if not email_or_phone:
            raise ValueError('The given email_or_phone must be set')

        if "@" in email_or_phone:
            email_or_phone = self.normalize_email(email_or_phone)
            username, email, phone = (email_or_phone, email_or_phone, "")
        else:
            phone = self.normalize_phone(
                email_or_phone, country_code=extra_fields.get("country_code"))
            username, email, phone = (email_or_phone, "", email_or_phone)

        now = timezone.now()
        is_active = extra_fields.pop("is_active", True)
        user = self.model(
            username=username,
            email=email,
            phone=phone,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now(),
            date_joined=now(),
            graph_lib='dygraph',
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email_or_phone, password=None, **extra_fields):
        return self._create_user(email_or_phone, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email_or_phone, password, **extra_fields):
        return self._create_user(email_or_phone, password, True, True,
                                 **extra_fields)


class AbstractEmailPhoneUser(AbstractBaseUser, PermissionsMixin):

    """ Abstract User with the same behaviour as Django's default User."""

    username = models.CharField(
        _('email or phone'), max_length=255, unique=True, db_index=True,
        help_text=_('Required. 255 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[validators.RegexValidator(
            r'^[\w.@+-]+$', _(
                'Enter a valid username. '
                'This value may contain only letters, numbers '
                'and @/./+/-/_ characters.'
            ), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    name = models.CharField(_('name'), max_length=255, blank=True)
    email = models.EmailField(_('email'), blank=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('active'), default=True, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = EmailPhoneUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """ Return the full name for the user."""
        return self.name

    def get_short_name(self):
        """ Return the short name for the user."""
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class EmailPhoneUser(AbstractEmailPhoneUser):

    """ Concrete class of AbstractEmailPhoneUser.

    Use this if you don't need to extend EmailPhoneUser.

    """

    class Meta(AbstractEmailPhoneUser.Meta):
        swappable = 'AUTH_USER_MODEL'
