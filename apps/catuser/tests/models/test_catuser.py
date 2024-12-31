import pytest

from apps.catuser.models import CatUser

@pytest.mark.django_db
class TestCatUser(object):
    def test_catuser_create_normal_user(self):
        catuser = CatUser.objects.create_user(
            email='Ih4bM@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )
        assert catuser.email == 'Ih4bM@example.com'
        assert catuser.first_name == 'John'
        assert catuser.last_name == 'Doe'
        assert catuser.is_staff is False
        assert catuser.is_active is True
        assert catuser.is_superuser is False

    def test_catuser_create_superuser(self):
        catuser = CatUser.objects.create_superuser(
            email='Ih4bM@example.com',
            password='password',
            first_name='John',
            last_name='Doe',
            is_superuser=True
        )
        assert catuser.email == 'Ih4bM@example.com'
        assert catuser.first_name == 'John'
        assert catuser.last_name == 'Doe'
        assert catuser.is_staff is True
        assert catuser.is_active is True
        assert catuser.is_superuser is True

    def test_catuser_invalid_email(self):
        with pytest.raises(ValueError):
            CatUser.objects.create_user(
                email=None,
                password='password',
                first_name='John',
                last_name='Doe',
                is_superuser=True
            )

    def test_catuser_superuser_invalid_flags(self):
        with pytest.raises(ValueError):
            CatUser.objects.create_superuser(
                email='Ih4bM@example.com',
                password='password',
                first_name='John',
                last_name='Doe',
                is_superuser=False,
                is_staff=False
            )

        with pytest.raises(ValueError):
            CatUser.objects.create_superuser(
                email='Ih4bM@example.com',
                password='password',
                first_name='John',
                last_name='Doe',
                is_superuser=False,
                is_staff=True
            )

    def test_catuser_string_representation(self):
        catuser = CatUser.objects.create_user(
            email='Ih4bM@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )
        assert str(catuser) == 'Ih4bM@example.com'
