package generator

import (
	"fmt"
	"reflect"

	"github.com/atombender/go-jsonschema/pkg/codegen"
	"github.com/atombender/go-jsonschema/pkg/schemas"
)

type output struct {
	file          *codegen.File
	declsByName   map[string]*codegen.TypeDecl
	declsBySchema map[*schemas.Type]*codegen.TypeDecl
	warner        func(string)
}

func (o *output) findExistingTypeDecl(name string, aType *interface{}) (*codegen.TypeDecl, bool) {
	declFound, ok := o.declsByName[name]

	if !ok || (ok && declFound.Type == nil) {
		return nil, false
	}

	var structureEquals bool = false
	switch declFound.Type.(type) {
	case codegen.PrimitiveType:
		val := reflect.ValueOf(aType)
		elem := val.Elem().Elem()
		id := elem.FieldByName("Id").String()
		structureEquals = aType != nil && declFound.Id != "" && declFound.Id == id
	default:
		structureEquals = aType != nil && reflect.DeepEqual(declFound.Type, *aType)
	}

	if structureEquals {
		return declFound, false
	}

	return nil, true
}

func (o *output) uniqueTypeName(name string, aType *interface{}) string {
	existingDecl, nameConflict := o.findExistingTypeDecl(name, aType)

	if !nameConflict {
		if existingDecl == nil {
			return name
		}
		return existingDecl.Name
	}

	count := 1

	for {
		suffixed := fmt.Sprintf("%s_%d", name, count)
		if _, ok := o.declsByName[suffixed]; !ok {
			o.warner(fmt.Sprintf(
				"Multiple types map to the name %q; declaring duplicate as %q instead", name, suffixed))

			return suffixed
		}

		count++
	}
}
