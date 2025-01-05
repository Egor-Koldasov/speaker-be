package utilstruct

func ForceMapStringKeysDeep(mapArg map[string]interface{}) error {
	var err error
	for key, value := range mapArg {
		if valueMap, ok := value.(map[interface{}]interface{}); ok {
			mapArg[key], err = ForceMapStringKeysRecursive(valueMap)
		}
		if err != nil {
			return err
		}
	}
	return nil
}
