#!/bin/bash

# To run this script: ./script.sh <path-to-create-venv>

set -e

if [ -z "$1" ]; then
    echo "Usage: ./script.sh <path-to-create-venv>"
    exit
fi


# Install and start memcached
brew install memcached

cp ./scripts/homebrew.mxcl.memcached.plist /usr/local/opt/memcached/

brew services start memcached

# Setup venv
virtualenv $1
source $1/bin/activate

pip install -r requirements.txt
