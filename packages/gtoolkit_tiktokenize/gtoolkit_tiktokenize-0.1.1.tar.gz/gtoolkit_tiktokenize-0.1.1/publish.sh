#!/bin/bash

echo "running publish gtoolkit_tiktokenize PyPI script"

# requirements: 
# - python3 (apt install python)
# - curl (apt install curl)
# - jq (apt install jq)
# - flit (pip install flit)

source_version=`cd src && python3 -c 'from gtoolkit_tiktokenize import __version__; print(__version__)'`
published_version=`curl -s https://pypi.org/pypi/gtoolkit_tiktokenize/json | jq -r .info.version`

if [ $source_version = $published_version ]
then
  echo "no action" $source_version "=" $published_version
else
  echo "publishing" $published_version ">" $source_version
  # FLIT_PASSWORD must already be set to token pypi-...
  FLIT_USERNAME=__token__ python3 -m flit publish
  echo "publish done"
fi
