import z from 'zod/v3'

export enum FsrsProgressState {
  Learning = 1,
  Review = 2,
  Relearning = 3,
}

export const fsrsProgressStateSchema = z.nativeEnum(FsrsProgressState)
