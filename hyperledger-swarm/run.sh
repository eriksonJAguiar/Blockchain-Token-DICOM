docker stack deploy -c hyperledger-zookeeper.yaml hyperledger-zk
docker stack deploy -c hyperledger-kafka.yaml hyperledger-kafka
docker stack deploy -c hyperledger-orderer.yaml hyperledger-orderer
docker stack deploy -c hyperledger-couchdb.yaml hyperledger-couchdb
docker stack deploy -c hyperledger-peer.yaml hyperledger-peer
docker stack deploy -c hyperledger-ca.yaml hyperledger-ca
docker stack deploy -c hyperledger-cli.yaml hyperledger-cli
