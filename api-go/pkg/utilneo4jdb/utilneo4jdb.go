package utilneo4jdb

import (
	"api-go/pkg/utilerror"
	"fmt"
	"maps"
	"reflect"
	"strings"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j/dbtype"
)

type NodeDefinition struct {
	Query  string
	Params map[string]any
}

func NodeProperties(varName string, nodeStruct interface{}, overrides *map[string]string) NodeDefinition {
	nameSpace := varName + "__"

	nodeMapNameSpaced := map[string]any{}
	var nodePropertyDefinitionStrings []string

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
			utilerror.LogErrorIf("Structs are not allowed", field.Kind() == reflect.Struct || field.Kind() == reflect.Map)

			utilerror.LogErrorIf("Arrays are not allowed", field.Kind() == reflect.Array || field.Kind() == reflect.Slice)
			if field.Kind() == reflect.String {
				fieldValue := field.String()
				nodeMapNameSpaced[nameSpace+fieldName] = string(fieldValue)
				nodePropertyDefinitionStrings = append(nodePropertyDefinitionStrings, fieldName+": $"+nameSpace+fieldName)
			}
		}
	}

	if overrides != nil {
		for key := range *overrides {
			nodePropertyDefinitionStrings = append(nodePropertyDefinitionStrings, key+":"+(*overrides)[key])
		}
	}

	nodePropertyDefinitions := strings.Join(nodePropertyDefinitionStrings, ", ")
	query := fmt.Sprintf(`{ %v }`, nodePropertyDefinitions)

	return NodeDefinition{
		Query:  query,
		Params: nodeMapNameSpaced,
	}
}

func CreateNodeDefinition(varName string, typeNames []string, nodeStruct interface{}, overrides *map[string]any) NodeDefinition {

	nameSpace := varName + "__"

	nodeMapNameSpaced := map[string]any{}
	var nodePropertyDefinitionStrings []string

	subQueries := ""

	refValNodeMap := reflect.ValueOf(nodeStruct)
	if refValNodeMap.Kind() == reflect.Pointer {
		if !refValNodeMap.IsNil() {
			refValNodeMap = refValNodeMap.Elem()
		}
	}
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
				if field.IsNil() {
					continue
				}
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
				subQueries += "\n" + CreateRelation(varName, nameSpace+fieldName, "HAS")
			}

			if field.Kind() == reflect.Array || field.Kind() == reflect.Slice {
				if field.IsNil() {
					continue
				}
				for j := 0; j < field.Len(); j++ {
					subField := field.Index(j)
					fieldValue := subField.Interface()
					if subField.Kind() == reflect.String {
						nodeMapNameSpaced[nameSpace+fieldName] = field.Interface()
						nodePropertyDefinitionStrings = append(nodePropertyDefinitionStrings, fieldName+": $"+nameSpace+fieldName)
						break
					} else {
						nodeDefinition := CreateNodeDefinition(nameSpace+fieldName+fmt.Sprint(j), []string{typeNames[0] + fieldName, "ListItem"}, fieldValue, &map[string]any{
							"Index": j,
						})
						maps.Copy(nodeMapNameSpaced, nodeDefinition.Params)
						subQueries += "\n" + nodeDefinition.Query
						subQueries += "\n" + CreateRelation(varName, nameSpace+fieldName+fmt.Sprint(j), "HAS")
					}
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

func CreateRelation(fromVarName string, toVarName string, relationName string) string {
	properties := NodeProperties(fromVarName, nil, &map[string]string{
		"CreatedAt": "datetime()",
	})
	return fmt.Sprintf(`
		CREATE (%v)-[:%v %v]->(%v)
`, fromVarName, relationName, properties.Query, toVarName)
}
func Relation(fromVarName string, toVarName string, relationName string, props map[string]any) NodeDefinition {
	properties := NodeProperties(fromVarName, props, nil)
	nodeDefinition := NodeDefinition{
		Query: fmt.Sprintf(`
		(%v)-[:%v %v]->(%v)
	`, fromVarName, relationName, properties.Query, toVarName),
		Params: properties.Params,
	}
	return nodeDefinition
}

func Match(varName string, typeNames []string, where map[string]any) NodeDefinition {
	nodeProps := NodeProperties(varName, where, nil)
	return NodeDefinition{
		Query:  fmt.Sprintf(`MATCH (%v %v)`, varName, nodeProps.Query),
		Params: nodeProps.Params,
	}
}

func AppendQuery(nodeDefinition NodeDefinition, queryies ...string) NodeDefinition {
	query := strings.Join(queryies, "")
	return NodeDefinition{
		Query:  nodeDefinition.Query + query,
		Params: nodeDefinition.Params,
	}
}

func RecordToModelMap(recordMap dbtype.Node) map[string]any {
	modelMap := map[string]any{}

	for propKey := range recordMap.Props {
		modelMap[propKey] = recordMap.Props[propKey]
	}

	return modelMap
}
