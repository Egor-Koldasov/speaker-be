#!bash

scriptDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"/"
(cd $scriptDir../json-schema/ && yarn generate) &&
(sh $scriptDir../api-go/scripts/go-jsonschema.sh)
