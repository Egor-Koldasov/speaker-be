import { AppError } from "../property/AppError";

export interface MessageBase {
  input: {
    name: string;
    data: object;
  };
  output: {
    name: string;
    data: object | null;
    errors: AppError[];
  };
}
