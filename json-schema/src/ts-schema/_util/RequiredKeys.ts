/**
 * Make selected keys required
 */
export type RequiredKeys<
  Obj extends object,
  Key extends keyof Required<Obj>,
> = Omit<Obj, Key> & { [K in Key]: Obj[K] };
