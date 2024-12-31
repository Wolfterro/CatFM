import pytest

from apps.catuser.models import CatUser


@pytest.fixture
def catuser():
    return CatUser.objects.create_user(
        email='Ih4bM@example.com',
        password='password',
        first_name='John',
        last_name='Doe'
    )
