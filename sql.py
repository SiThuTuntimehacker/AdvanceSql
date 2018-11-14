import requests
import re
import io
import os
import string

file = io.open('vulnsql.txt' , 'r')
err_list = file.readlines()
file.close()
print '''\033[1;93m
 ____  _ _____ _
/ ___|(_)_   _| |__  _   _
\___ \| | | | | '_ \| | | |
 ___) | | | | | | | | |_| |
|____/|_| |_| |_| |_|\__,_|
\033[1;32m
'''

file = io.open('url_pars.txt', 'w')
file.close()

dorks = io.open('dorklist.txt' , 'r', encoding='utf8')
dorks_list = dorks.readlines()
dorks.close()

pages = int(input('Input number of page: '))*10
print('Select number of dork: '+str(len(dorks_list)))
for i in range(len(dorks_list)):
    search = dorks_list[i].strip()
    count = 1
    while (count < pages):
        req = ('http://www.bing.com/search?q=' + search + '&first='+str(count))
        try:	
            response = requests.get(req)
        except:
            print('Error')
        req = ''	
        try:
            link = re.findall('<h2><a href="(.+?)"', response.text, re.DOTALL)
            for i in range(len(link)):
                print(link[i])
                if link[i].find('http://bs.yandex.ru'):
                    open('url_pars.txt', 'a+').write(link[i] +'\'' + '\n')
        except:
            print('Error parsing url')
        count = count+10

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

print '''\033[0;36m
 ____  _ _____ _
/ ___|(_)_   _| |__  _   _
\___ \| | | | | '_ \| | | |
 ___) | | | | | | | | |_| |
|____/|_| |_| |_| |_|\__,_|
'''
print('Please wait searching vuln site')
input = io.open('url_pars.txt', 'r')
output = io.open('searchinglist.txt', 'w')
linesarray = input.readlines()
input.close()
seen = []
seen = f7(linesarray)
for i in range(len(seen)):
    output.write(seen[i])
os.remove('url_pars.txt')
output.close()
print('Complete')
print('Checking Vuln...')

file = io.open('searchinglist.txt' , 'r')
url_list = file.readlines()
file.close()

err_page = 0
good_page = 0
for i in range(len(url_list)):
    page = url_list[i].strip()
    try:
        response = requests.get(page)
    except:
        err_page = err_page+1
        print('internet connection error.')
    for i in range(len(err_list)):
        err = str(err_list[i])
        err = err.strip()			
        if response.text.find(err)>0:
            print('\033[1;32mVuln\033[0m "'+err+'" in '+page)
            io.open('Vulnlist.txt', 'a+').write(page + '\n')
            good_page = good_page + 1
        else:
            pass

print('\n\033[1;97mVuln Site: '+str(good_page))
print('\n\033[1;97m404,403,406 pages: '+str(err_page))
print('\n\033[1;97mScan Complete')

