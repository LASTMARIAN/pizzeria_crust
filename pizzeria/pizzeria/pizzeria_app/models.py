# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Asiakas(models.Model):
    asiakas_id = models.AutoField(db_column='asiakas_ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    nimi = models.CharField(max_length=60)
    puhnumero = models.CharField(max_length=20)
    sahkoposti = models.CharField(max_length=60)
    osoite = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'asiakas'


class Juomat(models.Model):
    juoma_id = models.AutoField(db_column='juoma_ID', primary_key=True)  # Field name made lowercase.
    nimi = models.CharField(max_length=80)
    tilavuus = models.FloatField()
    hinta = models.IntegerField()
    kuva = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'juomat'


class Login(models.Model):
    admin_id = models.AutoField(db_column='admin_ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'login'


class Pizzat(models.Model):
    pizza_id = models.AutoField(db_column='pizza_ID', primary_key=True)  # Field name made lowercase.
    nimi = models.CharField(max_length=80)
    koko = models.CharField(max_length=50)
    taytteet = models.CharField(max_length=100)
    hinta = models.IntegerField()
    kuva = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pizzat'


class Tilaus(models.Model):
    tilaus_id = models.AutoField(db_column='tilaus_ID', primary_key=True)  # Field name made lowercase.
    asiakas = models.ForeignKey(Asiakas, models.DO_NOTHING, db_column='asiakas_ID')  # Field name made lowercase.
    hinta = models.DecimalField(max_digits=65, decimal_places=0)
    pvm = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tilaus'


class Tilausrivi(models.Model):
    tilriv_id = models.AutoField(db_column='tilRiv_ID', primary_key=True)  # Field name made lowercase.
    pizza = models.ForeignKey(Pizzat, models.DO_NOTHING, db_column='pizza_ID', blank=True, null=True)  # Field name made lowercase.
    juoma = models.ForeignKey(Juomat, models.DO_NOTHING, db_column='juoma_ID', blank=True, null=True)  # Field name made lowercase.
    tilaus = models.ForeignKey(Tilaus, models.DO_NOTHING, db_column='tilaus_ID')  # Field name made lowercase.
    pizzamaara = models.IntegerField(db_column='pizzaMaara')  # Field name made lowercase.
    juomamaara = models.IntegerField(db_column='juomaMaara')  # Field name made lowercase.
    hintapizzarivi = models.IntegerField(db_column='hintaPizzaRivi')  # Field name made lowercase.
    hintajuomarivi = models.IntegerField(db_column='hintaJuomaRivi')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tilausrivi'
