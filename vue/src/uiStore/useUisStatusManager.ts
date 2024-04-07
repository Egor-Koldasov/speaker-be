import { defineStore } from 'pinia'

export const useUisStatusManager = defineStore('uisStatusManager', {
  state: () => ({
    modal: {
      open: false,
    },
    form: {
      rootNodeId: '',
      status: {
        nodeId: '',
      },
    },
  }),
})
