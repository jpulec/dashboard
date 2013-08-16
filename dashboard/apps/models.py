from django.db import models
import datetime
from fabric.operations import sudo, run
from fabric.state import env
from fabric.context_managers import settings, show, hide
from fabric.network import disconnect_all

# Create your models here.

class ServiceGroup(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Environment(models.Model):
    name = models.CharField(max_length=4)
    service_group = models.ForeignKey('ServiceGroup')
    last_updated = models.DateTimeField(default=datetime.datetime.now())

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
    environment = models.ForeignKey('Environment')

    def __unicode__(self):
        return self.display_name + ":" + self.status

class ServiceTest(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        abstract = True

class SSHTest(ServiceTest):
    host = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name + " to be performed as user " + self.username + " on " + self.host

class ServiceCommand(models.Model):
    cmd = models.CharField(max_length=256)
    validate_func_str = models.CharField(max_length=256)
    failed_validation = models.TextField()
    execution_number = models.IntegerField()

    class Meta:
        abstract = True

    def execute(self):
        raise NotImplementedError

    def validate(self, result):
        raise NotImplementedError

    def __unicode__(self):
        return self.cmd + " to be performed as step " + str(self.execution_number)

class SSHCommand(ServiceCommand):
    sudo = models.BooleanField()

    class Meta:
        abstract = True

    def validate(self, result):
        try:
            return SSHResult.objects.get(container=self, result=result).response
        except Exception as e:
            pass

    def execute(self, pipe=None):
        with settings(hide('everything', 'status', 'stdout', 'stderr', 'commands'), warn_only=True, host_string=self.test.host, user=self.test.username, password=self.test.password):
            try:
                out = None
                if self.sudo:
                    out = sudo(self.cmd)
                else:
                    out = run(self.cmd)
            finally:
                disconnect_all()
        return self.validate(out)

    def __unicode__(self):
        return super(SSHCommand, self).__unicode__() + " as part of " + str(self.test)

class SSHResult(models.Model):
    result = models.CharField(max_length=256, db_index=True)
    response = models.CharField(max_length=256, db_index=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.result + " should respond with " + self.response
