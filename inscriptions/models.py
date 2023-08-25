from django.db import models
from Accounts.models import Student 
from courses.models import Level , Element , Module
# Create your models here.



class InscriptionAnnuelle(models.Model):
    idInscription = models.BigAutoField(primary_key=True)
    year = models.IntegerField()
    state = models.IntegerField()
    mention = models.CharField(max_length=255, null=True)
    plusInfos = models.CharField(max_length=255, null=True)
    rank = models.IntegerField()
    type = models.CharField(max_length=255, null=True)
    validation = models.CharField(max_length=255, null=True)
    idStudent = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    idLevel = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'inscriptionannuelle'
        managed = True

class InscriptionMatiere(models.Model):
    idInscriptionMatiere = models.BigAutoField(primary_key=True)
    coefficient = models.FloatField()
    noteFinale = models.FloatField(default=-1)
     #-1 as the default value to indicate that a valid score has not been provided yet for these fields.
    noteSN = models.FloatField(default=-1)
    noteSR = models.FloatField(default=-1)
    plusInfos = models.CharField(max_length=255, null=True)
    validation = models.CharField(max_length=255, null=True)
    idInscription = models.ForeignKey(InscriptionAnnuelle, on_delete=models.CASCADE, null=True)
    idMatiere = models.ForeignKey(Element, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'inscriptionmatiere'
        managed = True

class InscriptionModule(models.Model):
    idInscriptionModule = models.BigAutoField(primary_key=True)
    noteFinale = models.FloatField(default=-1) #I didn't find a double field 
    noteSN = models.FloatField(default=-1)
    noteSR = models.FloatField(default=-1)
    plusInfos = models.CharField(max_length=255, null=True)
    validation = models.CharField(max_length=255, null=True)
    idInscription = models.ForeignKey('InscriptionAnnuelle', on_delete=models.CASCADE, null=True)
    idModule = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'inscriptionmodule'
        managed = True

    def __str__(self):
        return f"InscriptionModule {self.idInscriptionModule}"