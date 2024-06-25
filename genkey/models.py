from django.db import models

# Create your models here.
class APIDoc(models.Model):
    username = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    request_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

def save(self, *args, **kwargs):
        # Automatically deactivate API key after 10 days
        if self.created_on < timezone.now() - timedelta(days=10):
            self.is_active = False
        super(APIDoc, self).save(*args, **kwargs)

def __str__(self):
        return f'{self.username} - {self.api_key}'





class Meta:
        verbose_name = "API Document"
        verbose_name_plural = "API Documents"
        ordering = ['-created_on']