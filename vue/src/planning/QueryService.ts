class QueryService {
  wsService: WsService

  constructor(wsService: WsService) {
    this.wsService = wsService
  }

  sendQuery(wsMessage)
}
