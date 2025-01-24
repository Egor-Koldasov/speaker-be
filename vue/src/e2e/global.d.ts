import { makeIdb } from '../idb/idb'

// Add cutom properties to window object
declare global {
  interface Window {
    idbPromise: ReturnType<typeof makeIdb>
  }
}
