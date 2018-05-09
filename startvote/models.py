from django.db import models

class Artivle(models.Model):
    title = models.CharField(max_length=32,default='title')
    content = models.TextField(null=True)
    pub_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'default'