from jinja2 import Template
from yaml import load
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

f=open('devices.yml', 'r')
my_vars = load(f.read())
f.close()

f=open('telemetry.j2')
my_template = Template(f.read())
f.close()

f=open('telemetry.conf','w')
f.write(my_template.render(my_vars))
f.close()

for item in my_vars['jti']['devices']:
    device=Device (host=item['out_of_band'], user=my_vars['jti']['username'], password=my_vars['jti']['password'])
    device.open()
    cfg=Config(device)
    cfg.load(path='telemetry.conf', format='set')
    cfg.commit()
    device.close()
    print 'configured device ' + item['out_of_band'] + ' with telemetry server ip ' +  my_vars['jti']['telemetry_server_ip']

