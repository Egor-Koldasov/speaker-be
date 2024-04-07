import { defineStore } from 'pinia'
import { TaskType, type Task, MSchemaTask } from '../crdt/idb/models/models'
import { assignUpdate } from '../util/assignUpdate'
import { addUpdate } from '../swClient/addUpdate'
import { omit } from 'lodash'
import { actionMap } from '../crdt/idb/actionMap'

const initForm = () => ({
  Name: '',
  CategoryId: null,
  Type: TaskType.Deadline,
  Estimate: 0,
  Note: '',
})
export const useUisTaskForm = defineStore('uisTaskForm', {
  state: () => ({
    form: initForm(),
    closed: true,
  }),
  actions: {
    toTask(): Task {
      return {
        ...MSchemaTask.default(undefined),
        Name: this.form.Name,
        CategoryId: this.form.CategoryId === 'null' ? null : this.form.CategoryId,
        Type: this.form.Type,
        Estimate: this.form.Estimate,
        Note: this.form.Note,
      }
    },
    submit() {
      void addUpdate(actionMap.CreateTask.create(this.toTask()))
      this.reset()
    },
    reset() {
      assignUpdate(this.form, omit(initForm(), ['categoryId', 'type', 'estimate']))
    },
  },
})
