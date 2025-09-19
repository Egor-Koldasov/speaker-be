import { proxy, useSnapshot } from 'valtio'
import { v7 as uuidV7 } from 'uuid'
import { useEffect } from 'react'

export type LocalProxyState<T> = {
  config: {
    initialValue: T
  }
  data: Record<string, T>
}

export const makeLocalProxy = <T>(initialValue: T) => {
  const initialProxyMap: LocalProxyState<T> = {
    config: {
      initialValue,
    },
    data: {},
  }

  return proxy(initialProxyMap)
}

export const useLocalProxy = <T>(
  stateMap: LocalProxyState<T>,
  id = uuidV7(),
) => {
  const snapMap = useSnapshot(stateMap)

  useEffect(() => {
    return () => {
      delete stateMap.data[id]
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  const snap = snapMap.data[id]

  if (!stateMap.data[id]) {
    stateMap.data[id] = structuredClone(stateMap.config.initialValue)
  }

  const state = stateMap.data[id]

  return { state, snap }
}
