import { schema } from "../_util/schema";

export default schema({
  title: "DbId",
  type: "string",
  description:
    'SurrealDb Id string with a format "Table:uuid". Where `uuid` is UUID v7 string',
});
