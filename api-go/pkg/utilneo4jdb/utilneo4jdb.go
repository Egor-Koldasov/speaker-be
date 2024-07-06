package utilneo4jdb

import (
	"fmt"
	"maps"
	"reflect"
	"strings"
)

type NodeDefinition struct {
	Query  string
	Params map[string]any
}

func CreateNodeDefinition(varName string, typeNames []string, nodeStruct interface{}, overrides *map[string]any) NodeDefinition {

	nameSpace := varName + "__"

	nodeMapNameSpaced := map[string]any{}
	var nodePropertyDefinitionStrings []string

	subQueries := ""

	refValNodeMap := reflect.ValueOf(nodeStruct)
	if refValNodeMap.Kind() == reflect.Struct || refValNodeMap.Kind() == reflect.Map {
		isStruct := refValNodeMap.Kind() == reflect.Struct
		numFields := 0
		if isStruct {
			numFields = refValNodeMap.NumField()
		} else {
			numFields = len(refValNodeMap.MapKeys())
		}
		for i := 0; i < numFields; i++ {
			var field reflect.Value
			fieldName := ""

			if isStruct {
				field = refValNodeMap.Field(i)
				fieldName = refValNodeMap.Type().Field(i).Name
			} else {
				field = refValNodeMap.MapIndex(refValNodeMap.MapKeys()[i])
				fieldName = refValNodeMap.MapKeys()[i].String()
			}
			if field.Kind() == reflect.Pointer {
				field = field.Elem()
			}
			if field.Kind() == reflect.Interface {
				field = field.Elem()
			}
			if field.Kind() == reflect.Struct || field.Kind() == reflect.Map {
				fieldValue := field.Interface()
				nodeDefinition := CreateNodeDefinition(nameSpace+fieldName, []string{typeNames[0] + fieldName}, fieldValue, nil)
				maps.Copy(nodeMapNameSpaced, nodeDefinition.Params)
				subQueries += "\n" + nodeDefinition.Query
				subQueries += "\n" + Relation(varName, nameSpace+fieldName, "HAS")
			}

			if field.Kind() == reflect.Array || field.Kind() == reflect.Slice {
				for j := 0; j < field.Len(); j++ {
					fieldValue := field.Index(j).Interface()
					nodeDefinition := CreateNodeDefinition(nameSpace+fieldName+fmt.Sprint(j), []string{typeNames[0] + fieldName, "ListItem"}, fieldValue, &map[string]any{
						"Index": j,
					})
					maps.Copy(nodeMapNameSpaced, nodeDefinition.Params)
					subQueries += "\n" + nodeDefinition.Query
					subQueries += "\n" + Relation(varName, nameSpace+fieldName+fmt.Sprint(j), "HAS")
				}
			}
			if field.Kind() == reflect.String {
				fieldValue := field.String()
				nodeMapNameSpaced[nameSpace+fieldName] = string(fieldValue)
				nodePropertyDefinitionStrings = append(nodePropertyDefinitionStrings, fieldName+": $"+nameSpace+fieldName)
			}
		}
	}
	if overrides != nil {
		for key := range *overrides {
			nodePropertyDefinitionStrings = append(nodePropertyDefinitionStrings, key+": $"+nameSpace+key)
			nodeMapNameSpaced[nameSpace+key] = (*overrides)[key]
		}
	}
	nodePropertyDefinitionStrings = append(nodePropertyDefinitionStrings, "CreatedAt: datetime()")

	nodePropertyDefinitions := strings.Join(nodePropertyDefinitionStrings, ", ")
	query := fmt.Sprintf(`
		CREATE (%v:%v { %v })
	`, varName, strings.Join(typeNames, ":"), nodePropertyDefinitions) + subQueries

	return NodeDefinition{
		Query:  query,
		Params: nodeMapNameSpaced,
	}
}

func Join(nodeDefinitions ...NodeDefinition) NodeDefinition {
	var queries []string
	var params map[string]any = map[string]any{}
	for _, nodeDefinition := range nodeDefinitions {
		queries = append(queries, nodeDefinition.Query)
		for key := range nodeDefinition.Params {
			params[key] = nodeDefinition.Params[key]
		}
	}
	return NodeDefinition{
		Query:  strings.Join(queries, "\n"),
		Params: params,
	}
}

func Relation(fromVarName string, toVarName string, relationName string) string {
	return fmt.Sprintf(`
			CREATE (%v)-[:%v { CreatedAt: datetime() }]->(%v)
		`, fromVarName, relationName, toVarName)
}
