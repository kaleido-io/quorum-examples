# vagrant cannot access this for some reason
sudo chmod 0666 /etc/hosts

sudo mkdir /gethipc
sudo chown vagrant:vagrant /gethipc

nodeDirs=(node-*/)
echo ${nodeDirs[0]}
echo ${nodeDirs[1]}
for i in {1..3}
do
    DDIR=/vagrant/backups/${nodeDirs[$i]}qdata
    CMD="constellation-node --url=https://127.0.0.$i:900$i/ --port=900$i --workdir=$DDIR --socket=/gethipc/constellation$i.ipc --publickeys=$DDIR/constellation/tm.pub --privatekeys=$DDIR/constellation/tm.key --storage="dir:$DDIR/constellation/data" --othernodes=https://127.0.0.1:9001/"
    echo "$CMD >> /tmp/constellation$i.log 2>&1 &"
    $CMD >> "/tmp/constellation$i.log" 2>&1 &

done

for i in {1..3}
do
DDIR=/vagrant/backups/${nodeDirs[$i]}qdata
nohup geth --nodiscover \
--datadir $DDIR/ethereum \
--nodekey $DDIR/ethereum/nodekey \
--maxpeers 200 \
--txpool.pricelimit 0 \
--rpc \
--port 2100${i} \
--rpcport 85${i}5 \
--rpcaddr 0.0.0.0 \
--ws \
--wsport 85${i}6 \
--wsaddr 0.0.0.0 \
--unlock 0 \
--password $DDIR/ethereum/passwords.txt \
--bootnodes enode://a75846059292db37d784b71f28f5e9165cf1b66f76be68f06254cbcaefe15f2bcb94663cf131d28c42f2559b35e2811b68e32ed9afe96e677d001fb896fb91c2@127.0.0.1:21001 \
--ipcpath=/gethipc/geth${i}.ipc \
--permissioned \
--syncmode full \
--mine \
--rpcapi admin,db,eth,debug,miner,net,shh,txpool,personal,web3,istanbul \
--wsapi admin,db,eth,debug,miner,net,shh,txpool,personal,web3,istanbul \
--istanbul.blockperiod 10 \
--istanbul.requesttimeout 20000 \
--rpccorsdomain '*' \
--wsorigins '*' \
--targetgaslimit 804247552 \
--gasprice 0 \
--txpool.globalslots 128 \
--txpool.accountslots 16 \
--txpool.globalqueue 32 \
--txpool.accountqueue 64 \
--cache 64 \
--trie-cache-gens 60 \
--networkid 528843285 \
--verbosity 4 2>>/tmp/${i}.log &
done
