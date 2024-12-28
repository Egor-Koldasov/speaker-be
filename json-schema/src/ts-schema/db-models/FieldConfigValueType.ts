import { schema } from "../_util/schema";

export enum FieldConfigValueTypes {
  Text = "Text",
  Image = "Image",
  Audio = "Audio",
}
export default schema({
  title: "FieldConfigValueType",
  type: "string",
  enum: Object.values(FieldConfigValueTypes),
  description: "The type of the value for AI to generate",
});
