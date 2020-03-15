#!/bin/bash

set +x
export BYFN_CA1_PRIVATE_KEY=$(cd crypto-config/peerOrganizations/hprovider.healthcare.com/ca && ls *_sk)
export BYFN_CA2_PRIVATE_KEY=$(cd crypto-config/peerOrganizations/research.healthcare.com/ca && ls *_sk)
export IMAGE_TAG=1.4
export CHANNEL_NAME=healthchannel
set -x


docker stack deploy --compose-file docker-compose-ca-pc1.yaml ca-pc1
docker stack deploy --compose-file docker-compose-couch-pc1.yaml couch-pc1
docker stack deploy --compose-file docker-compose-cli-pc1.yaml pc1-services