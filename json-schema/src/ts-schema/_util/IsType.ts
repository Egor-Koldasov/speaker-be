export type IsType<Extected, Type extends Extected> = Type extends Extected
  ? Type
  : never;
