from sandbox import Sandbox
from sandbox.config import SandboxConfig
config = SandboxConfig('stderr','stdout','interpreter')
config.enable('regex')
config.enable('time')
config.enable('datetime')
config.enable('math')
config.enable('random')
items = ['urllib2','urllib','struct','base64','httplib','socket','_socket']
for item in items: config.allowModule(item)
config.allowModule('httplib')
config.allowModule('array','array')
config.allowModule('StringIO', 'StringIO')
config.allowModule('os','_get_exports_list')
config.allowModule('json','scanner','decoder')

config.recursion_limit = 3000
sandbox = Sandbox(config)

import pickle


f = open('/tmp/data')
code, locals_dict = pickle.load(f)
f.close()

sandbox.execute(code, locals=locals_dict)
