# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from tasks import runcode
from celery.result import AsyncResult
import models, forms

def index(request, locals_dict={}):
    res = runcode.apply_async((1,))
    return HttpResponse("lol %s"%res.id)


from django.core import serializers
#data = serializers.serialize("xml", SomeModel.objects.all())
def graph(request, node_id):
    res = models.Node.objects.get(id=node_id)
    
    nodes = []
    links = []
    found = [res]
    top = []
    while found:
        node = found.pop()
        for x in node.previous.all():
            if not x.src in nodes:
                links.append(x)
                found.append(x.src)
                nodes.append(x.src)
        if node.previous.count() == 0:
            top.append(node)
    
    found = [res]
    while found:
        node = found.pop()
        for x in node.next.all():
            if not x.dst in nodes:
                links.append(x)
                found.append(x.dst)
                nodes.append(x.dst)
    
    nodes.append(res)
    
    nodes = map(lambda x: {'id':x.id, 'title':x.title, 'code':x.code,'group':1}, nodes)
    links = map(lambda x: {'id':x.id, 'source': x.src.id, 'target':x.dst.id,'value':2}, links)
    top = map(lambda x: x.id, top)
    import json
    return HttpResponse(json.dumps({'top':top, 'nodes':nodes, 'links':links}))

import pickle
def dump_view(request, dump_id, path=""):
    dump = models.LinkDump.objects.get(id = dump_id)
    data = pickle.loads(dump.dump.encode('ascii'))
    
    #path = filter(None, path.split("/"))
    #while path:
    #    data = data[path.pop(0)]
    
    #import pprint
    #data = pprint.pformat(data)
    return render_to_response('ticker/dump_view.html', {'data':data, 'dump':dump, 'path':path})

def nodeedit(request, node_id, focus=None):
    node = models.Node.objects.get(id=node_id)
    if request.method == "POST":
        form = forms.NodeForm(request.POST, instance=node)
        if form.is_valid():
            form.save()
    else:
        form = forms.NodeForm(instance=node)
    
    if focus:
        dump = models.LinkDump.objects.get(id=focus)
    else:
        dump = None
    return render_to_response('ticker/node_edit.html', {'node':node,'form':form, 'dump':dump},context_instance=RequestContext(request))

def dump_run(request, dump_id):
    dump = models.LinkDump.objects.get(id = dump_id)
    
    if dump.rerun_of:
        data = dump.rerun_of.dump
    else:
        data = dump.dump
    data = pickle.loads(data.encode('ascii'))
    
    new = models.LinkDump()
    
    if dump.rerun_of:
        new.rerun_of = dump.rerun_of
    else:
        new.rerun_of = dump
    new.link = dump.link
    
    res = runcode.apply_async((new.link.dst.id,), kwargs={'follow_links':False, 'locals_dict':data})
    new.result_id = res.id
    new.save()
    
    return redirect('/node/%d/edit/focus/%d'%(new.link.dst.id, new.id))

def dump_focus(request, dump_id):
    dump = models.LinkDump.objects.get(id = dump_id)
    
    return render_to_response('ticker/dump_focus.html', {'dump':dump})

def dump_status(request, dump_id):
    dump = models.LinkDump.objects.get(id = dump_id)
    
    res = AsyncResult(dump.result)

    return render_to_response('ticker/dump_status.html', {'dump':dump, 'res':res})

def noderun(request, node_id=1):
    node = models.Node.objects.get(id=node_id)
    res = runcode.apply_async([node_id])
    return HttpResponse("lol")

def view(request, node_id):
    node = models.Node.objects.get(id=node_id)
    return render_to_response('ticker/view.html', {'node': node})
   
