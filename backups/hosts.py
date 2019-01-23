addHosts = ' e0asehfaza e0h5r99f9a e0fl4w4atd'

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
file_path = '/etc/hosts'
fh, abs_path = mkstemp()
with fdopen(fh,'w') as new_file:
    with open(file_path) as old_file:
        for line in old_file:
            if line.startswith('127.0.0.1'):
                line = line.rstrip() + addHosts + "\n"
            new_file.write(line)
remove(file_path)
move(abs_path, file_path)

