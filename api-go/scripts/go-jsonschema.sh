#!bash
scriptDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"/"
schemas=(
  "MessageParseText.schema.json"
  "MessageParseTextToForeign.schema.json"
  "MessageBase.schema.json"
)
schemaPaths=""

for schema in "${schemas[@]}"
do
  schemaPaths="$schemaPaths $scriptDir../../json-schema/schema/$schema"
done

schemaPaths=$(cd "$scriptDir../../json-schema/schema-gen" && find . -name "*.json")
schemaPathsAbsolute=""
schemaOutput=""

for schemaPath in $schemaPaths
do
  schemaRelPath=${schemaPath:2}
  echo "Adding schema ${schemaRelPath}"

  schemaId=${schemaRelPath%?????}
  outputFileName=$(tr \/ _ <<< $schemaId)
  schemaOutput="$schemaOutput --schema-output=${schemaId}=$scriptDir../pkg/jsonschema/${outputFileName}.go"
  schemaPathsAbsolute="$schemaPathsAbsolute $scriptDir../../json-schema/schema-gen/${schemaPath}"
done

echo ''
echo "Generating schemas"
echo "~/go/bin/go-jsonschema -t -p jsonschema $schemaOutput $schemaPathsAbsolute"
echo ''
~/go/bin/go-jsonschema -t -p jsonschema $schemaOutput $schemaPathsAbsolute
