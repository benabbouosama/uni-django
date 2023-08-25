from django.db import models
from django.contrib.auth.models import  UserManager , AbstractUser , Group, Permission
from django.db.models import Q
from .field_validator import c_validate_email , validate_phone_number , validate_username
from django.contrib.auth import get_user_model
from courses.models import Filiere
import os
# Create your models here.

def get_default_profile_picture():
    return os.path.join('profile_pictures', 'default.png')
class CustomUser(AbstractUser):
    idUser = models.BigAutoField(primary_key=True)
    cin = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    ArabicLast_name = models.CharField(max_length=255, null=True)
    picture = models.ImageField(upload_to='profile_pictures/%y/%m/%d/', null=True, default=get_default_profile_picture)
    first_name = models.CharField(max_length=255, null=True)
    ArabicFirst_name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, validators=[validate_phone_number])

    # Add unique related_name for the groups and user_permissions fields
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_set',  # Change this to a unique related_name
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='customuser_set',  # Change this to a unique related_name
        related_query_name='user',
    )

    class Meta:
        db_table = 'user'
        managed = True

    @property
    def get_full_name(self):
        full_name = self.idUser
        if self.first_name and self.last_name:
            full_name = self.last_name + " " + self.first_name
        return full_name
    
    def __str__(self):
        return str(self.last_name)

class Role(models.Model):
    idRole = models.BigAutoField(primary_key=True)
    nameRole = models.CharField(max_length=255, null=True)
    

    class Meta:
        db_table = 'Role'
        managed = True

    def __str__(self):
        return self.nameRole


class Account(models.Model):
    idAccount = models.BigAutoField(primary_key=True)
    accepteDemandeAutorisationAbsence = models.BooleanField(default=False)
    accountNonExpired = models.BooleanField(default=False)
    accountNonLocked = models.BooleanField(default=False)
    afficheEmail = models.BooleanField(default=True)
    affichePicture = models.BooleanField(default=True)
    credentialsNonExpired = models.BooleanField(default=True)
    disconnectAccount = models.BooleanField(default=True)
    enabled = models.BooleanField(default=False)
    login = models.CharField(max_length=150, unique=True, validators=[validate_username])
    password = models.CharField(max_length=255, null=True)
    idUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    idRole = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

    def check_password(self,psw):
        if psw == self.password :
            return True
        return False
    

    
    class Meta:
        db_table = 'Account'
        managed = True
    
    @property
    def get_user_role(self):
        if self.idRole is not None:
            return self.idRole.nameRole
        return "No Role Assigned"

        
    


class CadreAdministrateur(models.Model):
    grade = models.CharField(max_length=255)
    idCardreAdmin = models.BigAutoField(primary_key=True)
    User = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cadre_administrateur')

    class Meta:
        db_table = 'cadreadministrateur'
        managed = True

    def __str__(self):
        return self.grade
class Professor(models.Model):
    specialite = models.CharField(max_length=255, null=True)
    idEnseignant = models.BigAutoField(primary_key=True)

    # Define the foreign key relationship with the Utilisateur model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Professor')

    class Meta:
        db_table = 'Professor'
        managed = True
    @property
    def get_full_name(self):
        return self.user
    def __str__ (self):
        return self.user.last_name

class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(cne__icontains=query) | 
                         Q(dateNaissance__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs
    
class Student(models.Model):
    cne = models.CharField(max_length=255, null=True)
    dateNaissance = models.DateTimeField(null=True)
    idEtudiant = models.BigAutoField(primary_key=True)

    # Define the foreign key relationship with the Utilisateur model
    User = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Student')
    objects = StudentManager()
    class Meta:
        db_table = 'Student'
        managed = True
class CoordinatorFiliere(models.Model):
    idCoordinator = models.OneToOneField(Professor, on_delete=models.CASCADE, primary_key=True)
    filiereId = models.OneToOneField(Filiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'coordinatorfiliere'
        managed = True

    def __str__(self):
        return f"CoordinatorFiliere {self.idCoordinator} - {self.filiereId}"
    
class ModifEtudiantHistori(models.Model):
    idModif = models.BigAutoField(primary_key=True)
    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    cne = models.CharField(max_length=255, null=True)
    idStudent = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'modifetudianthistori'
        managed = True

    def __str__(self):
        return f"ModifEtudiantHistori {self.idModif} - {self.last_name} {self.first_name}"


