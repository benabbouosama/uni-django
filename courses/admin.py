from django.contrib import admin
from .models import Filiere, Level, Module, Element
from django.contrib import admin
from .models import News
from courses import forms
# Register your models here.


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ['idFiliere', 'titleFiliere', 'anneeaccreditation', 'anneeFinaccreditation', 'codeFiliere']
    search_fields = ['idFiliere', 'titleFiliere', 'anneeaccreditation', 'anneeFinaccreditation', 'codeFiliere']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['idLevel', 'title', 'alias', 'idFiliere', 'idNextLevel']
    search_fields = ['idLevel', 'title', 'alias', 'idFiliere__titleFiliere', 'idNextLevel__title']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['idModule', 'title', 'code', 'idNiveau']
    search_fields = ['idModule', 'title', 'code', 'idNiveau__title']

@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ['idMatiere', 'name', 'code', 'currentCoefficient', 'idModule']
    search_fields = ['idMatiere', 'name', 'code', 'currentCoefficient', 'idModule__title']


class NewsAdminForm(forms.NewsForm):
    class Meta:
        model = News
        fields = ('title', 'pdf')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'timestamp')

