import type { Task } from '../../crdt/idb/models/models'

export const isTaskClosed = (task: Task) => false
// task.statusesClosed.includes(task.status)
