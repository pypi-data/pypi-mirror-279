from time import perf_counter, sleep, time
from subprocess import run


start = perf_counter()
import tooltils
print(perf_counter() - start)

#logger       = tooltils.info.logger()
verify: bool = False

start = perf_counter()

with tooltils.requests.openConnection("httpbin.org", verify=verify) as conn:
    amount = tooltils.timeTest(conn.send, 20, page="/get")

t1 = perf_counter() - start + amount

print(t1, tooltils.timeTest(tooltils.requests.get, 20, url="httpbin.org/get", verify=verify) * 20, sep='\n')

"""

verify     = False
advContext = tooltils.requests.advancedContext(extraLogs=True)

start = perf_counter()

with tooltils.requests.openConnection('httpbin.org', verify=verify, advContext=advContext) as conn:
    print(conn.send('GET', '/redirect-to?url=httpbin.org/redirect-to?url=google.com').redirected)

end = perf_counter() - start

with tooltils.requests.urllib.request('httpbin.org/redirect-to?url=httpbin.org/redirect-to?url=google.com', 'GET', verify=verify, advContext=advContext) as req:
    print(req.send().redirected)

end2 = perf_counter() - (end + start)

print(end, end2, sep='\n')

"""

#with tooltils.requests.openConnection('file-examples.com', verify=False) as conn:
#    print(conn.send('DOWNLOAD', '/storage/fe1b802e1565fe057a1d758/2017/11/file_example_WAV_1MG.wav', override=True, write_binary=True, file_name='test.wav').path)

#print(tooltils.waveLength('test.wav'))
