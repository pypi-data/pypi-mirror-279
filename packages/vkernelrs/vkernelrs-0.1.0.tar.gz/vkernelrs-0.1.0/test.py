import vkernelrs

fs = vkernelrs.PyFs()
term = vkernelrs.PyTerm(fs)

def write_file(file, content):
    if isinstance(content, str):
        content = content.encode('utf-8')

    f = fs.open(file, 'w')
    f.write(content)
    f.close()

# Create the fs
print("Initializing the filesystem")
fs.mkdir('/home')
fs.mkdir('/home/user')
fs.mkdir('/usr')
fs.mkdir('/usr/bin')
fs.mkdir('/usr/lib')
fs.mkdir('/usr/include')
fs.mkdir('/tmp')
fs.mkdir('/var')
fs.mkdir('/var/log')
fs.mkdir('/var/tmp')
fs.mkdir('/etc')
fs.mkdir('/etc/init.d')
fs.mkdir('/etc/rc.d')
write_file('/etc/passwd', 'root:x:0:0:root:/root:/bin/bash\nuser:x:1000:1000:user:/home/user:/bin/bash\n')
write_file('/etc/shadow', 'root:$6$zvZ6Q7z7$3')
write_file('/etc/init.d/network', '#!/bin/bash\n')
write_file('/etc/init.d/ssh', '#!/bin/bash\n')
write_file('/etc/init.d/httpd', '#!/bin/bash\n')
write_file('/etc/init.d/mysql', '#!/bin/bash\n')
write_file('/etc/rc.d/rc.local', '#!/bin/bash\n')
write_file('/var/log/messages', '')
write_file('/var/log/secure', '')
write_file('/var/log/httpd.log', '')
write_file('/var/log/mysql.log', '')
write_file('/var/tmp/file1', '')
write_file('/var/tmp/file2', '')
write_file('/var/tmp/file3', '')

# Start the loop to interact with the terminal
while True:
    prompt = input('vkernelrs> ')
    if prompt == 'exit':
        break

    try:
        out = term.exec(prompt)
        print(out)
    except ValueError as e:
        print(e)
