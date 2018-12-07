from django.db import models

# Create your models here.
class BillboardData(models.Model):
    
    date = models.DateTimeField();
    artist = models.CharField(max_length = 100);
    isNew = models.BooleanField();
    lastPos = models.IntegerField();
    peakPos = models.IntegerField();
    rank = models.IntegerField();
    title = models.CharField(max_length = 100);
    weeks = models.IntegerField();
    
    def __str__(self):
        
        return '|{}|{}|'.format(self.artist, self.title)
    
    
    