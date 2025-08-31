import { asyncMap } from 'convex-helpers'
import { getManyFrom } from 'convex-helpers/server/relationships'
import { query } from './_generated/server'
import { requireUserByCtx } from './users'
import { requireById } from './utils/requireById'

export const getFsrsProgressList = query({
  async handler(ctx, args) {
    const user = await requireUserByCtx(ctx)
    const relSenseFsrsProgressList = await getManyFrom(
      ctx.db,
      'relSenseFsrsProgress',
      'byUserIdSenseId',
      user._id,
      'userId',
    )
    const fsrsProgressListLoaded = await asyncMap(
      relSenseFsrsProgressList,
      async (relSenseFsrsProgress) => {
        const fsrsProgress = await requireById(
          ctx.db,
          relSenseFsrsProgress.fsrsProgressId,
        )
        const sense = await requireById(ctx.db, relSenseFsrsProgress.senseId)

        const dictionaryEntry = await requireById(
          ctx.db,
          sense.dictionaryEntryId,
        )

        return {
          relSenseFsrsProgress,
          fsrsProgress,
          sense,
          dictionaryEntry,
        }
      },
    )

    return fsrsProgressListLoaded
  },
})
