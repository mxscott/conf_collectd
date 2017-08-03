import collectd
import random
import docker

PATH = '/sys/power/image_size'

def config_func(config):

    collectd.info('docker_container: setting up')



#    path_set = False

#    for node in config.children:
#        key = node.key.lower()
#        val = node.values[0]

#        if key == 'path':
#            global PATH
#            PATH = val
#            path_set = True
#        else:
#            collectd.info('custom_plugin: Unknown config key "%s"' % key)

#    if path_set:
#        collectd.info('custom_plugin: Using overridden path %s' % PATH)
#    else:
#        collectd.info('custom_plugin: Using default path %s' % PATH)


def read_func():
    client = docker.from_env()
    total_containers = len(client.containers.list(all=True))
    running_containers = len(client.containers.list())
    # Dispatch value to collectd
    val = collectd.Values()
    val.plugin = 'docker_container'
    val.type = 'containers'
    val.type_instance = 'total'
    val.dispatch(values=[total_containers])
	
    val.type_instance = 'running'
    val.dispatch(values=[running_containers])

    val.type = 'images'
    for im in client.images.list(all=True):
        val.type_instance = im.id
        num = len(client.containers.list(True, filters={'ancestor': im.id}))
        val.dispatch(values=[num])


collectd.register_config(config_func)
collectd.register_read(read_func)

