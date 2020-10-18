from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=140)
    mainDoctor = models.CharField(max_length=140)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']