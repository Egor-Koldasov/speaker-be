import { makeIdb } from '../src/idb/idb'

// Add cutom properties to window object
declare global {
  interface Window {
    idbPromise: ReturnType<typeof makeIdb>
  }
}
