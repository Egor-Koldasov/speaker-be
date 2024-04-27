import { ErrorName } from "./ErrorName";

export type AppError = {
  name: ErrorName;
  message: string;
};
