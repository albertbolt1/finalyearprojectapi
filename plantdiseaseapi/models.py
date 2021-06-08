from django.db import models

# Create your models here.
class PlantDiseaseImage(models.Model): 
	plantimage = models.ImageField(upload_to='images/')