# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Reference3846(models.Model):
    field_idrref = models.BinaryField(primary_key=True, db_column='_idrref')  # Field renamed because it started with '_'.
    field_version = models.IntegerField(db_column='_version')  # Field renamed because it started with '_'.
    field_marked = models.BooleanField(db_column='_marked')  # Field renamed because it started with '_'.
    field_predefinedid = models.BinaryField(db_column='_predefinedid')  # Field renamed because it started with '_'.
    field_parentidrref = models.BinaryField(db_column='_parentidrref')  # Field renamed because it started with '_'.
    field_folder = models.BooleanField(db_column='_folder')  # Field renamed because it started with '_'.
    field_code = models.TextField(db_column='_code')  # Field renamed because it started with '_'. This field type is a guess.
    field_description = models.TextField(db_column='_description')  # Field renamed because it started with '_'. This field type is a guess.
    field_fld3847 = models.TextField(db_column='_fld3847', blank=True, null=True)  # Field renamed because it started with '_'. This field type is a guess.
    field_fld3848 = models.TextField(db_column='_fld3848', blank=True, null=True)  # Field renamed because it started with '_'. This field type is a guess.
    field_fld3849 = models.TextField(db_column='_fld3849', blank=True, null=True)  # Field renamed because it started with '_'. This field type is a guess.
    field_fld3850 = models.TextField(db_column='_fld3850', blank=True, null=True)  # Field renamed because it started with '_'. This field type is a guess.
    field_fld3851 = models.TextField(db_column='_fld3851', blank=True, null=True)  # Field renamed because it started with '_'. This field type is a guess.
    field_fld210 = models.DecimalField(db_column='_fld210', max_digits=7, decimal_places=0)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = '_reference3846'
        unique_together = (('field_fld210', 'field_parentidrref', 'field_folder', 'field_code', 'field_idrref'), ('field_fld210', 'field_parentidrref', 'field_folder', 'field_description', 'field_idrref'), ('field_fld210', 'field_code', 'field_idrref'), ('field_fld210', 'field_description', 'field_idrref'), ('field_fld210', 'field_idrref'),)

