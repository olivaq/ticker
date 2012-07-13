from django.db import models

# Create your models here.

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
    
class LinkDump(models.Model):
    link = models.ForeignKey(Link, related_name="dumps")
    dump = models.TextField()
    result = models.TextField()
