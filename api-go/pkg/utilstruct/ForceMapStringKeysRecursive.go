package utilstruct

import "fmt"

func ForceMapStringKeysRecursive(mapArg map[interface{}]interface{}) (map[string]interface{}, error) {
	mapResult := map[string]interface{}{}
	for key, value := range mapArg {
		keyString, ok := key.(string)
		if !ok {
			return nil, fmt.Errorf("key is not a string: %v", key)
		}
		mapResult[keyString] = value
		if valueMap, ok := value.(map[interface{}]interface{}); ok {
			valueMap, err := ForceMapStringKeysRecursive(valueMap)
			if err != nil {
				return nil, err
			}
			mapResult[keyString] = valueMap
		}
	}
	return mapResult, nil
}
