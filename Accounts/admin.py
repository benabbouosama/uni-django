from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  CustomUser, Role, Account, CadreAdministrateur, Professor, Student, CoordinatorFiliere, ModifEtudiantHistori
# Register your models here.





admin.site.register(CustomUser)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Role)
admin.site.register(Account)
admin.site.register(CadreAdministrateur)
admin.site.register(CoordinatorFiliere)
admin.site.register(ModifEtudiantHistori)





