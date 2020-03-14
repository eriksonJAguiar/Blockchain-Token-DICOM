#!/bin/bash

CHANNEL_NAME=healthchannel
CONTRACT_PATH=/opt/gopath/src/github.com/chaincode/Dicom-contract
CONTRACT_NAME=Dicom-contract

CONFIG_ROOT=/opt/gopath/src/github.com/hyperledger/fabric/peer
HPROVIDER_MSPCONFIGPATH=${CONFIG_ROOT}/crypto-config/peerOrganizations/hprovider.healthcare.com/users/Admin@hprovider.healthcare.com/msp
HPROVIDER_TLS_ROOTCERT_FILE=${CONFIG_ROOT}/crypto-config/peerOrganizations/hprovider.healthcare.com/peers/peer0.hprovider.healthcare.com/tls/ca.crt
RESEARCH_MSPCONFIGPATH=${CONFIG_ROOT}/crypto-config/peerOrganizations/research.healthcare.com/users/Admin@research.healthcare.com/msp
RESEARCH_TLS_ROOTCERT_FILE=${CONFIG_ROOT}/crypto-config/peerOrganizations/research.healthcare.com/peers/peer0.research.healthcare.com/tls/ca.crt
ORDERER_TLS_ROOTCERT_FILE=${CONFIG_ROOT}/crypto-config/ordererOrganizations/healthcare.com/orderers/orderer.healthcare.com/msp/tlscacerts/tlsca.healthcare.com-cert.pem

CORE_PEER_TLS_ENABLED=true
ORDERER_CA=${CONFIG_ROOT}/crypto-config/ordererOrganizations/healthcare.com/orderers/orderer.healthcare.com/msp/tlscacerts/tlsca.healthcare.com-cert.pem

PEER0_HPROVIDER="docker exec
-e CORE_PEER_LOCALMSPID=HProviderMSP
-e CORE_PEER_ADDRESS=peer0.hprovider.healthcare.com:7051
-e CORE_PEER_MSPCONFIGPATH=${HPROVIDER_MSPCONFIGPATH}
-e CORE_PEER_TLS_ROOTCERT_FILE=${HPROVIDER_TLS_ROOTCERT_FILE}
cli
bash"

echo "Create channel ..."

docker exec -it -e CORE_PEER_LOCALMSPID=HProviderMSP -e CORE_PEER_ADDRESS=peer0.hprovider.healthcare.com:7051 -e CORE_PEER_MSPCONFIGPATH=${HPROVIDER_MSPCONFIGPATH} -e CORE_PEER_TLS_ROOTCERT_FILE=${HPROVIDER_TLS_ROOTCERT_FILE} -e CORE_PEER_TLS_ENABLED=${CORE_PEER_TLS_ENABLED} -e ORDERER_CA=${ORDERER_CA} cli peer channel create -o orderer.healthcare.com:7050 -c ${CHANNEL_NAME} -f ./channel-artifacts/channel.tx --tls --cafile $ORDERER_CA

sleep 2

#----------- Create Channel -------------

echo "join channel for peer0.hprovider ..."


docker exec  -e CORE_PEER_LOCALMSPID=HProviderMSP -e CORE_PEER_ADDRESS=peer0.hprovider.healthcare.com:7051 -e CORE_PEER_MSPCONFIGPATH=${HPROVIDER_MSPCONFIGPATH} -e CORE_PEER_TLS_ROOTCERT_FILE=${HPROVIDER_TLS_ROOTCERT_FILE} -e CORE_PEER_TLS_ENABLED=${CORE_PEER_TLS_ENABLED} -e ORDERER_CA=${ORDERER_CA} cli peer channel join -b ${CHANNEL_NAME}.block
docker exec -it cli peer channel join -b ${CHANNEL_NAME}.block

sleep 2

#---------- Instatiate chaincode ------------------

echo "Instatiate chaincode peer0.hprovider..."

docker exec  -e CORE_PEER_LOCALMSPID=HProviderMSP -e CORE_PEER_ADDRESS=peer0.hprovider.healthcare.com:7051 -e CORE_PEER_MSPCONFIGPATH=${HPROVIDER_MSPCONFIGPATH} -e CORE_PEER_TLS_ROOTCERT_FILE=${HPROVIDER_TLS_ROOTCERT_FILE} -e CORE_PEER_TLS_ENABLED=${CORE_PEER_TLS_ENABLED} -e ORDERER_CA=${ORDERER_CA} cli peer chaincode instantiate -o orderer.healthcare.com:7050 -C ${CHANNEL_NAME} -l node -n ${CONTRACT_NAME} -v 1.0 -c '{"Args":[]}'