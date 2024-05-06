#!bash

scriptDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"/"

fswatch -r -o --exclude './json-schema/gen*' --exclude './json-schema/dist' ./json-schema |\
xargs -n1 -I{} sh "${scriptDir}generate-json-schema.sh"
