import pytest
import re

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from trench.utils import create_secret, generate_backup_codes


User = get_user_model()


def pytest_addoption(parser):
    parser.addoption(
        "--hasher", action="store", default="PBKDF2", help="Options: PBKDF2, PBKDF2SHA1, Argon2 or BCrypt"
    )


@pytest.fixture()
def set_hasher(request, settings):
    parse_hasher: str = request.config.getoption("--hasher")
    hashers_list = settings.PASSWORD_HASHERS
    hashers_test: list = [hasher for hasher in hashers_list if re.search(parse_hasher, hasher, re.IGNORECASE)]

    if hashers_test:
        settings.PASSWORD_HASHERS = hashers_test
    else:
        raise ValueError(f"Cannot set the hasher to: {parse_hasher}")


@pytest.fixture()
def active_user_with_email_otp(set_hasher):
    user, created = User.objects.get_or_create(
        username='imhotep',
        email='imhotep@pyramids.eg',
    )
    if created:
        user.set_password('secretkey'),
        user.is_active = True
        user.save()

        MFAMethod = apps.get_model('trench.MFAMethod')
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=True,
            name='email',
            is_active=True,
        )

    return user


@pytest.fixture()
def active_user_with_sms_otp(set_hasher):
    user, created = User.objects.get_or_create(
        username='imhotep',
        email='imhotep@pyramids.eg',
        phone_number='555-555-555'
    )
    if created:
        user.set_password('secretkey'),
        user.is_active = True
        user.save()

        MFAMethod = apps.get_model('trench.MFAMethod')
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=True,
            name='sms',
            is_active=True,
        )

    return user


@pytest.fixture()
def active_user_with_email_and_inactive_other_methods_otp(set_hasher):
    user, created = User.objects.get_or_create(
        username='imhotep',
        email='imhotep@pyramids.eg',
    )
    if created:
        user.set_password('secretkey'),
        user.is_active = True
        user.save()

        MFAMethod = apps.get_model('trench.MFAMethod')
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=True,
            name='email',
            is_active=True,
        )
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=False,
            name='sms',
            is_active=False,
        )
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=False,
            name='app',
            is_active=False,
        )

    return user


@pytest.fixture()
def active_user_with_backup_codes(set_hasher):
    user, created = User.objects.get_or_create(
        username='cleopatra',
        email='cleopatra@pyramids.eg',
    )
    backup_codes = generate_backup_codes()
    encrypted_backup_codes = '-'.join([make_password(_) for _ in backup_codes])
    if created:
        user.set_password('secretkey'),
        user.is_active = True
        user.save()

        MFAMethod = apps.get_model('trench.MFAMethod')
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=True,
            name='email',
            is_active=True,
            _backup_codes=encrypted_backup_codes,
        )

    return user, backup_codes[0]


@pytest.fixture()
def active_user_with_many_otp_methods(set_hasher):
    user, created = User.objects.get_or_create(
        username='ramses',
        email='ramses@thegreat.eg',
    )
    backup_codes = generate_backup_codes()
    encrypted_backup_codes = '-'.join([make_password(_) for _ in backup_codes])
    if created:
        user.set_password('secretkey'),
        user.is_active = True
        user.save()

        MFAMethod = apps.get_model('trench.MFAMethod')
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=True,
            name='email',
            is_active=True,
            _backup_codes=encrypted_backup_codes,
        )
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=False,
            name='sms',
            is_active=True,
            _backup_codes=encrypted_backup_codes,
        )
        MFAMethod.objects.create(
            user=user,
            secret=create_secret(),
            is_primary=False,
            name='app',
            is_active=True,
            _backup_codes=encrypted_backup_codes,
        )
        MFAMethod.objects.create(
            user=user,
            is_primary=False,
            name='yubi',
            is_active=True,
            _backup_codes=encrypted_backup_codes,
        )

    return user, backup_codes[0]


@pytest.fixture()
def active_user(set_hasher):
    user, created = User.objects.get_or_create(
        username='hetephernebti',
        email='hetephernebti@pyramids.eg',
    )
    if created:
        user.set_password('secretkey'),
        user.is_active = True
        user.save()

    return user


@pytest.fixture()
def inactive_user(set_hasher):
    user, created = User.objects.get_or_create(
        username='djoser',
        email='djoser@pyramids.eg',
    )
    if created:
        user.set_password('secretkey'),
        user.is_active = False
        user.save()

    return user


@pytest.fixture()
def admin_user(set_hasher):
    return User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        is_active=True,
        password='secretkey',
    )
