import { defineStore } from 'pinia'
import type { ModelNode } from '../../../struct/gen/models'
import { uuidv7 } from '@kripod/uuidv7'
import { watchEffect } from 'vue'

type NodeForm = Omit<ModelNode, 'CreatedAt' | 'UpdatedAt'>

export type Coord = { x: number; y: number }
export type AlarmSettings = {
  nodeId: string
  date_end: string
}

const initState = () => ({
  selectedNodeId: null as string | null,
  movingNodeId: null as string | null,
  relSettingsNodeId: null as string | null,
  movingCoords: null as Coord | null,
  scrollBoxRef: null as HTMLDivElement | null,
  alarmSettings: null as AlarmSettings | null,
  draggingNodeId: null as string | null,
  newNodeFormShown: false,
  viewMode: 'folders' as 'folders' | null,
  nodeForm: {
    Id: uuidv7(),
    ContentShort: '',
    ContentLong: '',
    ParentId: null,
    RelFromIds: [],
    RelToIds: [],
    UserId: '',
    AlarmIds: [],
    DeletedAt: null,
  } satisfies NodeForm,
  nodePositionMap: {} as Record<
    string,
    {
      rect: DOMRect
    }
  >,
  drag: {
    draggingNodeId: null as string | null,
  },
  nodeFoldedMap: {} as { [K in string]?: boolean },
  scroll: { x: 0, y: 0 },
  initialized: false,
  style: {
    lvlColorBg: true,
    lvlColorLine: true,
  },
})
const useUisNodeMap_ = defineStore('uisNodeMap', {
  state: initState,
  actions: {
    initState() {
      const nodeFoldedMapString = localStorage.getItem('nodeFoldedMap')
      if (nodeFoldedMapString) {
        this.nodeFoldedMap = JSON.parse(nodeFoldedMapString)
      }
      const scrollString = localStorage.getItem('scroll')
      if (scrollString) {
        this.scroll = JSON.parse(scrollString)
      }
      this.initialized = true

      watchEffect(() => {
        localStorage.setItem('nodeFoldedMap', JSON.stringify({ ...this.nodeFoldedMap }))
      })
      watchEffect(() => {
        if (typeof window === 'undefined' || !this.scrollBoxRef) return
        this.scrollBoxRef.addEventListener('scroll', () => {
          if (!this.scrollBoxRef) {
            console.warn('scrollBoxRef not found')
            return
          }
          this.scroll = { x: this.scrollBoxRef.scrollLeft, y: this.scrollBoxRef.scrollTop }
          localStorage.setItem('scroll', JSON.stringify(this.scroll))
        })
      })
    },
  },
})

export const useUisNodeMap = () => {
  const uisNodeMap = useUisNodeMap_()
  if (!uisNodeMap.initialized) uisNodeMap.initState()
  return uisNodeMap
}
