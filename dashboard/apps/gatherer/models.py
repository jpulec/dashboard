from django.db import models

# Create your models here.

class ServiceGroup(models.Model):
    name = models.CharField(max_length=256)
    environment = models.ForeignKey('Environment')

    def __unicode__(self):
        return self.name + ":" + self.environment.name

    class Meta:
        unique_together = ("name", "environment",)

class Environment(models.Model):
    name = models.CharField(max_length=4)

    def __unicode__(self):
        return self.name

class ServiceStatus(models.Model):
    STATUS_CHOICES = (
            ('ok', "Ok"),
            ('warn', "Warning"),
            ('info', "Info"),
            ('error', "Error")
    )

    display_name = models.CharField(max_length=256)
    dttm = models.DateTimeField()
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
    status_description = models.TextField()
    service_group = models.ForeignKey('ServiceGroup')

    def __unicode__(self):
        return self.display_name + ":" + self.status
