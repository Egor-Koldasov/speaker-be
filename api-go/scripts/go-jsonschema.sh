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

schemaPaths=$(cd "$scriptDir../../json-schema/gen-schema-json" && find . -name "*.json" | sort -t '\0' -n)
schemaPathsAbsolute=""
schemaOutput=""

for schemaPath in $schemaPaths
do
  schemaRelPath=${schemaPath:2}
  echo "Adding schema ${schemaRelPath}"

  schemaId=$(basename ${schemaRelPath%?????})
  # Remove digits from the begining of the schemaId
  if [[ $schemaId =~ ^[0-9]+_(.*)$ ]]; then
    schemaId=${BASH_REMATCH[1]}
  fi
  outputFileName=$(tr \/ _ <<< $schemaId)
  schemaOutput="$schemaOutput --schema-output=${schemaId}=$scriptDir../pkg/genjsonschema/${outputFileName}.go"
  schemaPathsAbsolute="$schemaPathsAbsolute $scriptDir../../json-schema/gen-schema-json/${schemaPath}"
done

echo ''
echo "Generating schemas"
echo "~/go/bin/go-jsonschema -t -p genjsonschema $schemaOutput $scriptDir../../json-schema/gen-schema-json/Main.json"
echo ''
rm -rf $scriptDir../pkg/genjsonschema/*
$scriptDir../third_party/go-jsonschema/main -t -p genjsonschema $schemaOutput $scriptDir../../json-schema/gen-schema-json/Main.json
