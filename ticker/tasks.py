from celery import task
from ticker.models import *

from sandbox import Sandbox
from sandbox.config import SandboxConfig
config = SandboxConfig('stdout')
config.enable('regex')
config.enable('time')
config.enable('datetime')
config.enable('math')
config.enable('random')

import re
import pickle, os
@task()
def runcode(id, locals_dict={}, debug=False, follow_links=True):
    print locals_dict
    for k,v in locals_dict.items():
        print type(v)
    node = Node.objects.get(id=id)
    if node == None: raise Exception("Node not found")
    
    code = node.code.encode('ascii').replace("\r","")
    
    print "Running node %s"%node.title
    
    
    if os.path.exists(os.path.join('/home/oyvinbak/python/django_ticker/ticker/nodes', code)):
        path = os.path.join('/home/oyvinbak/python/django_ticker/ticker/nodes', code)
        print path
        f = open(path)
        exec f in locals_dict, locals_dict
        f.close()
    else:
        sandbox = Sandbox(config)
        sandbox.execute(code, globals=locals_dict)
    
    for k,obj in locals_dict.items():
        try:
            pickle.dumps(obj)
        except:
            del locals_dict[k]
    
    if debug: return
    
    if follow_links:
        for link in node.next.filter(enabled=True):
            res = runcode.apply_async([link.dst.id], {"locals_dict":locals_dict})
            if link.debug:
                ld = LinkDump()
                ld.link = link
                ld.dump = pickle.dumps(locals_dict)
                ld.result_id = res.id
                ld.save()
    else:
        print "Not following links"
        
    return locals_dict
