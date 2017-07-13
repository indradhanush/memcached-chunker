from pymemcache.client.base import Client

client = Client(('localhost', 11211))

set_result = client.set('foo', 'bar')
print "Setting foo: ", set_result

value = client.get('foo')
print "Retrieved value of foo: ", value

print "Max memory: ", client.stats()['limit_maxbytes']
