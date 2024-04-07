import { defineStore } from 'pinia'
import { debounce } from 'lodash'
import { addUpdate } from '../swClient/addUpdate'
import { actionMap } from '../crdt/idb/actionMap'

export const useUisTaskList = defineStore('uisTaskList', {
  state: () => ({
    selectedTaskId: null as string | null,
    estimateTaskId: null as string | null,
    manualTimeTaskId: null as string | null,
  }),
})

export const useOnTaskNameChange = (taskId: string) => {
  const onTaskNameChange = debounce(
    (nextName: string) => {
      void addUpdate(actionMap.UpdateTask.create({ Id: taskId, Name: nextName }))
    },
    1000,
    { leading: true, trailing: true },
  )
  return onTaskNameChange
}
