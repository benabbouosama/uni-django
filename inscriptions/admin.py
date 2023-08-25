from django.contrib import admin
from .models import InscriptionAnnuelle, InscriptionMatiere, InscriptionModule

# Register your models here.

class InscriptionAnnuelleAdmin(admin.ModelAdmin):
    list_display = ['idInscription', 'year', 'state', 'mention', 'plusInfos', 'rank', 'type', 'validation', 'idStudent', 'idLevel']
    search_fields = ['idInscription', 'year', 'state', 'mention', 'plusInfos', 'rank', 'type', 'validation', 'idStudent__User__username', 'idLevel__title']

class InscriptionMatiereAdmin(admin.ModelAdmin):
    list_display = ['idInscriptionMatiere', 'coefficient', 'noteFinale', 'noteSN', 'noteSR', 'plusInfos', 'validation', 'idInscription', 'idMatiere']
    search_fields = ['idInscriptionMatiere', 'coefficient', 'noteFinale', 'noteSN', 'noteSR', 'plusInfos', 'validation', 'idInscription__idInscription', 'idMatiere__name']

class InscriptionModuleAdmin(admin.ModelAdmin):
    list_display = ['idInscriptionModule', 'noteFinale', 'noteSN', 'noteSR', 'plusInfos', 'validation', 'idInscription', 'idModule']
    search_fields = ['idInscriptionModule', 'noteFinale', 'noteSN', 'noteSR', 'plusInfos', 'validation', 'idInscription__idInscription', 'idModule__title']

admin.site.register(InscriptionAnnuelle, InscriptionAnnuelleAdmin)
admin.site.register(InscriptionMatiere, InscriptionMatiereAdmin)
admin.site.register(InscriptionModule, InscriptionModuleAdmin)
