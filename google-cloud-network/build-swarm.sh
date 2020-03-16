#!/bin/bash

set +x
export BYFN_CA1_PRIVATE_KEY=$(cd crypto-config/peerOrganizations/hprovider.healthcare.com/ca && ls *_sk)
export BYFN_CA2_PRIVATE_KEY=$(cd crypto-config/peerOrganizations/research.healthcare.com/ca && ls *_sk)
export IMAGE_TAG=1.4
export CHANNEL_NAME=healthchannel
set -x


docker stack deploy --compose-file docker-compose-hlf-orderer.yaml orderer-node1
docker stack deploy --compose-file docker-compose-ca-pc1.yaml ca-node1
docker stack deploy --compose-file docker-compose-couch-pc1.yaml couch-node1
docker stack deploy --compose-file docker-compose-cli-pc1.yaml services-node1
docker stack deploy --compose-file docker-compose-hlf-cli.yaml cli-node1



docker stack deploy --compose-file docker-compose-couch-pc2.yaml couch-node2
docker stack deploy --compose-file docker-compose-cli-pc2.yaml services-node2


docker stack deploy --compose-file docker-compose-ca-pc2.yaml ca-pc2

docker stack deploy --compose-file docker-compose-couch-pc3.yaml couch-node3
docker stack deploy --compose-file docker-compose-cli-pc3.yaml services-node3


docker stack deploy --compose-file docker-compose-couch-pc4.yaml couch-node4
docker stack deploy --compose-file docker-compose-cli-pc4.yaml services-node4


