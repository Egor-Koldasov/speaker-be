package e2eutil

import "github.com/lxzan/gws"

type WsClient struct {
	conn *gws.Conn
}

func WsSendMessage[RequestMessage *any, ResponseMessage *any](
	wsClient *gws.Conn,
	requestMessage RequestMessage,
) (ResponseMessage, error) {
	return nil, nil
}
