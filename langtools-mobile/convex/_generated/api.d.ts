/* eslint-disable */
/**
 * Generated `api` utility.
 *
 * THIS CODE IS AUTOMATICALLY GENERATED.
 *
 * To regenerate, run `npx convex dev`.
 * @module
 */

import type {
  ApiFromModules,
  FilterApi,
  FunctionReference,
} from "convex/server";
import type * as fsrsProgress from "../fsrsProgress.js";
import type * as http from "../http.js";
import type * as internal_ from "../internal.js";
import type * as internalNode from "../internalNode.js";
import type * as types_AuthUser from "../types/AuthUser.js";
import type * as users from "../users.js";
import type * as utils_requireById from "../utils/requireById.js";
import type * as utils_requireId from "../utils/requireId.js";

/**
 * A utility for referencing Convex functions in your app's API.
 *
 * Usage:
 * ```js
 * const myFunctionReference = api.myModule.myFunction;
 * ```
 */
declare const fullApi: ApiFromModules<{
  fsrsProgress: typeof fsrsProgress;
  http: typeof http;
  internal: typeof internal_;
  internalNode: typeof internalNode;
  "types/AuthUser": typeof types_AuthUser;
  users: typeof users;
  "utils/requireById": typeof utils_requireById;
  "utils/requireId": typeof utils_requireId;
}>;
export declare const api: FilterApi<
  typeof fullApi,
  FunctionReference<any, "public">
>;
export declare const internal: FilterApi<
  typeof fullApi,
  FunctionReference<any, "internal">
>;
