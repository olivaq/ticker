from django.db import models
from datetime import datetime
from celery.result import AsyncResult
# Create your models here.
from pickle import loads

class Node(models.Model):
    title = models.CharField(max_length=255)
    code = models.TextField()
    def __str__(self):
        return self.title
    
class Link(models.Model):
    src = models.ForeignKey(Node, related_name="next")
    dst = models.ForeignKey(Node, related_name="previous")
    enabled = models.BooleanField()
    debug = models.BooleanField()
    def __str__(self):
        return "%s->%s"%(self.src.title, self.dst.title)
    
    def lastDumps(self):
        return self.dumps.order_by('-created')
    
class LinkDump(models.Model):
    link = models.ForeignKey(Link, related_name="dumps")
    dump = models.TextField()
    
    result_id = models.CharField(max_length=255, default="")
    
    created = models.DateTimeField(default=datetime.now)
    rerun_of = models.ForeignKey("LinkDump", null=True,blank=True)
    
    def loads(self):
        if self.rerun_of:
            return self.rerun_of.loads()
        return loads(self.dump.encode('ascii'))
    
    def result(self):
        return AsyncResult(self.result_id)
