import 'fake-indexeddb/auto'
import '../../mocks/mockServiceWorker'
import { beforeAll, describe } from 'vitest'
import { makeCrudTest } from '../../util/makeCrudTest'
import { dateStr } from '../../../util/datetime/dateStr'
import { testCreateNode } from '../../scenarios/testCreateNode'

const state = {
  nodeId: '',
  updateNodeId: '',
}
export const statusManagerTest = makeCrudTest(
  'StatusManager',
  () => ({
    RootNodeId: state.nodeId,
    CreatedAt: dateStr(),
    DeletedAt: null,
    UpdatedAt: dateStr(),
  }),
  () => ({
    RootNodeId: state.updateNodeId,
  }),
)
describe('StatusManager', () => {
  beforeAll(async () => {
    const { id: nodeId } = await testCreateNode()
    const { id: updateNodeId } = await testCreateNode()
    state.nodeId = nodeId
    state.updateNodeId = updateNodeId
  })
  statusManagerTest.Run()
})
