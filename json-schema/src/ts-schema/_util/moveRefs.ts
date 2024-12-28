export const moveRefs = <T extends object>(schema: T, relPrefix: string): T => {
  if ("$ref" in schema && schema.$ref) {
    schema.$ref = `${relPrefix}/${schema.$ref}`;
  }
  for (const key in schema) {
    const value = schema[key];
    if (typeof value === "object") {
      schema[key] = moveRefs(value as any, relPrefix);
    }
  }
  return schema;
};
