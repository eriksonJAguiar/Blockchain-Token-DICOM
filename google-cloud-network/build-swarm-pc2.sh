#!/bin/bash

set +x
export BYFN_CA1_PRIVATE_KEY=$(cd crypto-config/peerOrganizations/hprovider.healthcare.com/ca && ls *_sk)
export BYFN_CA2_PRIVATE_KEY=$(cd crypto-config/peerOrganizations/research.healthcare.com/ca && ls *_sk)
export IMAGE_TAG=1.4
export CHANNEL_NAME=healthchannel
set -x


docker stack deploy --compose-file docker-compose-ca-pc2.yaml ca-pc2
docker stack deploy --compose-file docker-compose-couch-pc2.yaml couch-pc2
docker stack deploy --compose-file docker-compose-cli-pc2.yaml pc2-services