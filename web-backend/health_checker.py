# get info dict about all running processes
import subprocess
output = subprocess.check_output(('TASKLIST', '/FO', 'CSV')).decode()
# get rid of extra " and split into lines
output = output.replace('"', '').split('\r\n')
keys = output[0].split(',')
proc_list = [i.split(',') for i in output[1:] if i]
# make dict with proc names as keys and dicts with the extra nfo as values
proc_dict = dict((i[0], dict(zip(keys[1:], i[1:]))) for i in proc_list)
for name, values in sorted(proc_dict.items(), key=lambda x: x[0].lower()):
    print('%s: %s' % (name, values))
