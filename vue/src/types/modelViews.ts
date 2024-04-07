import type { AllModelSchemas, ModelNode } from '../../../struct/gen/models'

export const mViewStatus = (
  status: AllModelSchemas['Status']['Model'],
  node: ModelNode | null,
) => ({
  ...status,
  node,
})
export type MViewStatus = ReturnType<typeof mViewStatus>
export const mViewStatusManager = (
  manager: AllModelSchemas['StatusManager']['Model'],
  rootNode: ModelNode | null,
  statuses: (Omit<MViewStatus, 'node'> & { node: ModelNode })[],
) => ({
  ...manager,
  rootNode,
  statuses,
})
export type MViewStatusManager = ReturnType<typeof mViewStatusManager>
