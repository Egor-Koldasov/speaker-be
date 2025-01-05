package unittest_test

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utildev"
	"api-go/pkg/utiljson"
	"api-go/pkg/utilstruct"
	"reflect"
	"testing"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

type LeafByKey map[string]TestLeaf1

type TestLeaf1 struct {
	StringProp string `json:"stringProp" yaml:"stringProp" mapstructure:"stringProp"`
	IntProp    int    `json:"intProp" yaml:"intProp" mapstructure:"intProp"`
}

type TestNode1 struct {
	StringProp string    `json:"stringProp" yaml:"stringProp" mapstructure:"stringProp"`
	IntProp    int       `json:"intProp" yaml:"intProp" mapstructure:"intProp"`
	Leaf1      TestLeaf1 `json:"leaf1" yaml:"leaf1" mapstructure:"leaf1"`
}
type TestNode2 struct {
	StringProp string     `json:"stringProp" yaml:"stringProp" mapstructure:"stringProp"`
	IntProp    int        `json:"intProp" yaml:"intProp" mapstructure:"intProp"`
	Leaf1      *TestLeaf1 `json:"leaf1,omitempty" yaml:"leaf1,omitempty" mapstructure:"leaf1,omitempty"`
}
type TestNode3 struct {
	StringProp string                `json:"stringProp" yaml:"stringProp" mapstructure:"stringProp"`
	IntProp    int                   `json:"intProp" yaml:"intProp" mapstructure:"intProp"`
	LeafByKey1 *map[string]TestLeaf1 `json:"leafByKey1,omitempty" yaml:"leafByKey1,omitempty" mapstructure:"leafByKey1,omitempty"`
}
type TestNode4 struct {
	StringProp string    `json:"stringProp" yaml:"stringProp" mapstructure:"stringProp"`
	IntProp    int       `json:"intProp" yaml:"intProp" mapstructure:"intProp"`
	LeafByKey1 LeafByKey `json:"leafByKey1,omitempty" yaml:"leafByKey1,omitempty" mapstructure:"leafByKey1,omitempty"`
}

func TestMapToModelNested(t *testing.T) {
	testMap1 := map[string]interface{}{
		"stringProp": "stringProp1",
		"intProp":    1,
		"leaf1": map[string]interface{}{
			"stringProp": "stringProp1.1",
			"intProp":    11,
		},
	}
	testMap2 := map[string]interface{}{
		"stringProp": "stringProp2",
		"intProp":    2,
		"leaf1": map[string]interface{}{
			"stringProp": "stringProp2.1",
			"intProp":    21,
		},
	}
	testMap3 := map[string]interface{}{
		"stringProp": "stringProp3",
		"intProp":    3,
		"leafByKey1": map[string]map[string]interface{}{
			"key1": {
				"stringProp": "stringProp3.1",
				"intProp":    31,
			},
		},
	}
	testMap4 := map[string]any{
		"stringProp": "stringProp4",
		"intProp":    4,
		"leafByKey1": map[string]map[string]interface{}{
			"key1": {
				"stringProp": "stringProp4.1",
				"intProp":    41,
			},
		},
	}
	testLensCardConfig := map[string]interface{}{
		"createdAt": "2021-01-01T00:00:00Z",
		"deletedAt": nil,
		"fieldConfigByName": map[interface{}]interface{}{
			"field1": map[string]interface{}{
				"createdAt": "2021-01-01T00:00:00Z",
				"deletedAt": nil,
				"id": models.RecordID{
					Table: "FieldConfig",
					ID:    "test-1",
				},
				"maxResult": 3,
				"minResult": 1,
				"name":      "test-field-1",
				"prompt":    "test-prompt-1",
				"updatedAt": "2021-01-01T00:00:00Z",
				"valueType": "Text",
			},
		},
		"id":        "LensCardConfig:test-1",
		"name":      "test-card-1",
		"updatedAt": "2021-01-01T00:00:00Z",
		"userId":    "User:test-1",
	}

	utilstruct.ForceMapStringKeysDeep(testLensCardConfig)

	testNode1 := utilstruct.TranslateStruct[TestNode1](testMap1)
	testNode2 := utilstruct.TranslateStruct[TestNode2](testMap2)
	testNode3 := utilstruct.TranslateStruct[TestNode3](testMap3)
	testNode4 := utilstruct.TranslateStruct[TestNode4](testMap4)
	testMap4Json := utiljson.MarshalIndent(testMap4)
	testLensCardConfigModel :=
		surrealdbutil.MapToModel[genjsonschema.LensCardConfig](testLensCardConfig)
	testLensCardConfigJson := utiljson.MarshalIndent(testLensCardConfig)
	testLensCardConfigFieldMapRefl := reflect.ValueOf(testLensCardConfig["fieldConfigByName"])
	type_ := testLensCardConfigFieldMapRefl.Type()
	typeKind := type_.Kind()
	valKind := testLensCardConfigFieldMapRefl.Kind()
	utildev.KeepUnusedVars(map[string]any{
		"type":     type_,
		"valKind":  valKind,
		"typeKind": typeKind,
	})

	if testNode1.Leaf1.StringProp != "stringProp1.1" {
		t.Errorf("Expected stringProp1.1, got %s", testNode1.Leaf1.StringProp)
	}

	if testNode2.Leaf1.StringProp != "stringProp2.1" {
		t.Errorf("Expected stringProp2.1, got %s", testNode2.Leaf1.StringProp)
	}

	if (*testNode3.LeafByKey1)["key1"].StringProp != "stringProp3.1" {
		t.Errorf("Expected stringProp3.1, got %s", (*testNode3.LeafByKey1)["key1"].StringProp)
	}

	if testNode4.LeafByKey1["key1"].StringProp != "stringProp4.1" {
		t.Errorf("Expected stringProp4.1, got %s", testNode4.LeafByKey1["key1"].StringProp)
	}

	if testLensCardConfigModel.FieldConfigByName["field1"].Name != "test-field-1" {
		t.Errorf("Expected test-field-1, got %s", testLensCardConfigModel.FieldConfigByName["field1"].Name)
	}

	if testMap4Json == "" {
		t.Errorf("Expected json string, got empty string")
	}

	if testLensCardConfigJson == "" {
		t.Errorf("Expected json string, got empty string")
	}
}
