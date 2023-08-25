from django.db import models
from django.urls import reverse
from django.db.models import Q


# Create your models here.
class Filiere(models.Model):
    idFiliere = models.BigAutoField(primary_key=True)
    anneeFinaccreditation = models.IntegerField()
    anneeaccreditation = models.IntegerField()
    codeFiliere = models.CharField(max_length=255, null=True)
    titleFiliere = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Filiere'
        managed = True

    def __str__(self):
        return f"Filiere {self.titleFiliere}"


class Level(models.Model):
    idLevel = models.BigAutoField(primary_key=True)
    alias = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    idFiliere = models.ForeignKey(Filiere, on_delete=models.CASCADE, null=True)
    idNextLevel = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Level'
        managed = True

    def __str__(self):
        return f"Level {self.title}"

class Module(models.Model):
    idModule = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    idNiveau = models.ForeignKey(Level, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Module'
        managed = True

    def __str__(self):
        return f"Module {self.title}"

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    
    def pdf_file_upload_path(instance, filename):
        sanitized_filiere = instance.filiere.titleFiliere.replace(':', '-')
        sanitized_level = instance.level.title.replace(':', '-')
        sanitized_module = instance.module.title.replace(':', '-')
        return f'course_pdfs/{sanitized_filiere}/{sanitized_level}/{sanitized_module}/{filename}'
    
    pdf_file = models.FileField(upload_to=pdf_file_upload_path, null=True, blank=True)

    
class Element(models.Model):
    idMatiere = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=255, null=True)
    currentCoefficient = models.FloatField(default=1.0)
    name = models.CharField(max_length=255, null=True)
    idModule = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Element'
        managed = True

    def __str__(self):
        return f"Element {self.name}"



class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='news_pdfs/')
    class Meta:
        db_table = 'News'
        managed = True

    def __str__(self):
        return self.title

