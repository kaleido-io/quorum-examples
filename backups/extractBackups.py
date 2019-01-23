import json
nodePrefix = 'node-'

#remove node directories
import os, re, shutil
pattern = 'node-'
for f in os.listdir('.'):
    if re.search(pattern, f):
        shutil.rmtree(f)

# extract nodes again
import tarfile
for fname in os.listdir('.'):
    if fname.endswith('.tgz'):
        nodeId = fname.split('-')[1]
        nodeDir = nodePrefix + nodeId
        tar = tarfile.open(fname, "r:gz")
        os.mkdir(nodeDir)
        tar.extractall(path=nodeDir)
        tar.close()


for fname in os.listdir('.'):
    if fname.startswith(nodePrefix):
        nodePath = '%s/qdata/' % (fname)
        with open(nodePath + 'boot.config') as f:
            bootConfig = json.load(f)
        bootConfig["bootnode"] = 'enode://a75846059292db37d784b71f28f5e9165cf1b66f76be68f06254cbcaefe15f2bcb94663cf131d28c42f2559b35e2811b68e32ed9afe96e677d001fb896fb91c2@e0asehfaza:30303'
        with open(nodePath + 'boot.config', 'w') as f:
            f.write(json.dumps(bootConfig))

        # switch master in 'boot.config' and 'constellation/tm.conf'
        
        filenames = ['ethereum/static-nodes.json',
                'ethereum/permissioned-nodes.json',
                'permissioned-nodes.json',
                'constellation/tm.conf',
                ]
        
        removePaths = ['/constellation/tm.conf.tmp',
                'ethereum/geth/nodes'
                ]
        
        replacements = [
                # encoded node identifiers
                ("100.67.123.77:30303?raftport=50400", "e0asehfaza:30303?raftport=50400"),
                ("100.66.5.16:30303?raftport=50400", "e0h5r99f9a:30304?raftport=50401"),
                ("100.67.87.88:30303?raftport=50400", "e0fl4w4atd:30305?raftport=50402"),
                # constellation urls
                ("100.67.123.77:9000", "e0asehfaza:9000"),
                ("100.66.5.16:9000", "e0h5r99f9a:9001"),
                ("100.67.87.88:9000", "e0fl4w4atd:9002"),
                # constellation othernodes
                ("100.69.11.79:9000", "127.0.0.1:9001"),
                # contellation socket fixup to absolute
                ("../gethipc", "/gethipc")
                ]
        
        for filename in filenames:
            for frum,tu in replacements:
                with open(nodePath + filename) as f:
                    newText=f.read().replace(frum, tu)
                with open(nodePath + filename, "w") as f:
                    f.write(newText)
        
        # put all keys into localhost for tls files
        import json
        tlsFiles = ['tls-known-servers', 'tls-known-clients']
        for file_path in tlsFiles:
            with open(nodePath + file_path) as f:
                data = json.load(f)
            newData = {'hosts' : {'127.0.0.1': [] }}
            for host in data['hosts']
                newData['hosts']['127.0.0.1'].append(data['hosts'][host][0])
            with open(nodePath + file_path, 'w') as f:
                f.write(json.dumps(newData))

