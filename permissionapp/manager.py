from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager( BaseUserManager ):
    def create_user(self, user_name, email_id, password=None, **extra_fields):
        if not email_id:
            raise ValueError( 'The Email field must be set' )
        email_id = self.normalize_email( email_id )
        user = self.model( user_name=user_name, email_id=email_id, **extra_fields )
        user.set_password( password )
        user.save( using=self._db )
        return user

    def create_superuser(self, user_name, email_id, password=None, **extra_fields):
        extra_fields.setdefault( 'is_staff', True )
        extra_fields.setdefault( 'is_superuser', True )

        if extra_fields.get( 'is_staff' ) is not True:
            raise ValueError( 'Superuser must have is_staff=True.' )
        if extra_fields.get( 'is_superuser' ) is not True:
            raise ValueError( 'Superuser must have is_superuser=True.' )

        return self.create_user( user_name, email_id, password, **extra_fields )
