package e2eutil

import (
	"api-go/pkg/utilerror"

	"github.com/lxzan/gws"
)

const serverURL = "ws://localhost:6969/ws"

func WsClient(handler *gws.Event) (*gws.Conn, error) {

	// Dial the WebSocket server
	conn, _, err := gws.NewClient(*handler, &gws.ClientOption{
		Addr: serverURL,
	})
	if utilerror.LogError("Failed to connect to WebSocket server: %v\n", err) {
		return nil, err
	}

	return conn, nil
}
