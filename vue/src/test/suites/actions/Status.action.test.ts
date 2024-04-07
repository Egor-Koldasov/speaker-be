import 'fake-indexeddb/auto'
import '../../mocks/mockServiceWorker'
import { beforeAll, describe } from 'vitest'
import { makeCrudTest } from '../../util/makeCrudTest'
import { dateStr } from '../../../util/datetime/dateStr'
import { statusManagerTest } from './StatusManager.action.test'
import { testCreateNode } from '../../scenarios/testCreateNode'
import { StatusType } from '../../../../../struct/gen/models'

const state = {
  managerId: '',
  nodeId1: '',
  nodeId2: '',
}
const test = makeCrudTest(
  'Status',
  () => ({
    ManagerId: state.managerId,
    NodeId: state.nodeId1,
    Type: StatusType.Inactive,
    CreatedAt: dateStr(),
    DeletedAt: null,
    UpdatedAt: dateStr(),
  }),
  () => ({
    Type: StatusType.Active,
  }),
)
describe('Status', () => {
  beforeAll(async () => {
    const { id: managerId } = await statusManagerTest.testCreate()
    const { id: nodeId1 } = await testCreateNode()
    const { id: nodeId2 } = await testCreateNode()

    state.managerId = managerId
    state.nodeId1 = nodeId1
    state.nodeId2 = nodeId2
  })
  test.Run()
})
