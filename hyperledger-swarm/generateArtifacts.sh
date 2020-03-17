#!/bin/bash +x
#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#


#set -e
set -e

#FABRIC_CFG_PATH="configtx.yaml" # Config used by configtxgen
CRYPTO_CONFIG="crypto-config.yaml"

PROFILE=HealthOrdererGenesis
CHANNEL_PROFILE=HealthChannel
export CHANNEL_NAME=healthchannel
export BYFN_CA1_PRIVATE_KEY=$(cd crypto-config/peerOrganizations/hprovider.healthcare.com/ca && ls *_sk)
export BYFN_CA2_PRIVATE_KEY=$(cd crypto-config/peerOrganizations/research.healthcare.com/ca && ls *_sk)
ORGANIZATION_NAME=(HProviderMSP ResearchMSP)
export FABRIC_ROOT=${PWD}
export FABRIC_CFG_PATH=${PWD}
echo

# Print the usage message
function printHelp () {
  echo "Usage: "
	echo "  generateArtifacts.sh [-c <channel name>] [-d <domain name>] [-o <number of orgs]"
  echo "  generateArtifacts.sh -h|--help (print this message)"
  echo "    -c <channel name> - channel name to use (defaults to \"mychannel\")"
  echo "    -d <domain name> - domain name to use (defaults to \"example.com\")"
	echo "    -o <number of orgs> - number of organizations to use (defaults to \"2\")"
  echo
  echo "Taking all defaults:"
  echo "	generateArtifacts.sh"
}

OS_ARCH=$(echo "$(uname -s|tr '[:upper:]' '[:lower:]'|sed 's/mingw64_nt.*/windows/')-$(uname -m | sed 's/x86_64/amd64/g')" | awk '{print tolower($0)}')

## Using docker-compose template replace private key file names with constants
function replacePrivateKey () {
	ARCH=`uname -s | grep Darwin`
	if [ "$ARCH" == "Darwin" ]; then
		OPTS="-it"
	else
		OPTS="-i"
	fi

	#cp docker-compose-e2e-template.yaml docker-compose-e2e.yaml
  #cp hyperledger-swarm-template.yaml hyperledger-swarm.yaml
	NUM_ORGS=(hprovider, research)
	while [ "$i" -le "$NUM_ORGS" ]; do
		CURRENT_DIR=$PWD
  	cd crypto-config/peerOrganizations/${i}.healthcare.com/ca/
  	PRIV_KEY=$(ls *_sk)
  	cd $CURRENT_DIR
  	#sed $OPTS "s/CA1_PRIVATE_KEY/${PRIV_KEY}/g" docker-compose-e2e.yaml
		sed $OPTS "s/CA_${i}_PRIVATE_KEY/${PRIV_KEY}/g" hyperledger-ca.yaml
	done
}

# 1. Generate crypto-config Folder containing all CA, PEER, TLS, NETWORK ADMIN, certificate etc.
function generateCert(){
  rm -Rf ./crypto-config
  mkdir ./crypto-config

  set -x
  ../bin/cryptogen generate --config=./$CRYPTO_CONFIG
  res=$?
  set +x
  if [ $res -ne 0 ]; then
    echo "Failed to generate certificates..."
    exit 1
  fi
}

# 2. Create Genesis block with initial consortium definition and anchorPeers
function generateChannelArtifacts() {

  rm -Rf ./channel-artifacts
  mkdir ./channel-artifacts

  # Create Genesis block defined by profile OrgsOrdererGenesis in configtx.yaml
  set -x
  ../bin/configtxgen -profile $PROFILE -outputBlock ./channel-artifacts/genesis.block
  res=$?
  set +x
  if [ $res -ne 0 ]; then
    echo "Failed to generate orderer genesis block..."
    exit 1
  fi

  # Create initial channel configuration defined by profile OrgsChannel in configtx.yaml
  set -x
  ../bin/configtxgen -profile $CHANNEL_PROFILE -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID $CHANNEL_NAME
  res=$?
  set +x
  if [ $res -ne 0 ]; then
    echo "Failed to generate channel configuration transaction..."
    exit 1
  fi

  # Create anchorPeer configuration defined in profile OneOrgChannel in configtx.yaml
  for i in ${!ORGANIZATION_NAME[@]}; do
    set -x
    ../bin/configtxgen -profile $CHANNEL_PROFILE -outputAnchorPeersUpdate ./channel-artifacts/${ORGANIZATION_NAME[$i]}-anchors.tx -channelID $CHANNEL_NAME -asOrg ${ORGANIZATION_NAME[$i]}
    res=$?
    set +x
    if [ $res -ne 0 ]; then
      echo "Failed to generate ${ORGANIZATION_NAME[$i]} Anchor peer configuration transaction..."
      exit 1
    fi
  done

}

generateCert
replacePrivateKey
generateChannelArtifacts
