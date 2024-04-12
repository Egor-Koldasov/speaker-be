export const isNodeOrParent = (node: Node, parent: Node): boolean => {
  if (node === document.body) {
    return false
  }
  if (node === parent) {
    return true
  }
  if (!node.parentNode) {
    return false
  }
  return isNodeOrParent(node.parentNode, parent)
}
