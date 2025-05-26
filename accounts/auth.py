from rest_framework.exceptions import AuthenticationFailed, APIException

from django.contrib.auth.hashers import check_password, make_password

from accounts.models import User

from companies.models import Enterprise, Employee


class Authentication:
    def signin(self, email=None, password=None) -> User:
        exception_auth = AuthenticationFailed('Email e/ou senha incorreto(s)')

        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            raise exception_auth
        
        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise exception_auth
        
        return user
    
    def signup(self, name, email, password, type_account='owner', company_id=False):
        if not name or name == '':
            raise APIException('O nome não deve ser null')
        
        if not email or email == '':
            raise APIException('O nome não deve ser null')
        
        if not password or password == '':
            raise APIException('O nome não deve ser null')
        
        user = User
        if user.objects.filter(email=email).exists():
            raise APIException('Esse email já existe na plataforma')
        
        password_hashed = make_password(password)

        created_user = user.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=0 if type_account == 'employee' else 1
        )

        return created_user