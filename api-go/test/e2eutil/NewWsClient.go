package e2eutil

import (
	"api-go/pkg/broadcastchan"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"api-go/pkg/utiljson"
	"api-go/pkg/utillog"
	"api-go/pkg/utilstruct"
	"errors"
	"testing"
	"time"

	"github.com/lxzan/gws"
)

const serverURL = "ws://localhost:6969/ws"

type WsClientRunnerHelper struct {
	conn        *gws.Conn
	MessageChan chan *gws.Message
}

func (runnerHelper *WsClientRunnerHelper) Request(
	requestMessage interface{},
) (interface{}, error) {
	requestBase := utilstruct.TranslateStruct[genjsonschema.WsMessageBase](requestMessage)
	if requestBase.Id == "" {
		return nil, errors.New("Request message ID is empty")
	}
	requestBytes := []byte(utiljson.Marshal(requestMessage))
	runnerHelper.conn.WriteMessage(gws.OpcodeText, requestBytes)

	for {

	}
}

type WsClientRunner struct {
	Run func(helper *WsClientRunnerHelper)
	// OnMessage func(message *gws.Message)
}

func NewWsClient(t *testing.T, runner *WsClientRunner) error {
	helper := WsClientRunnerHelper{MessageChan: make(chan *gws.Message)}
	runnerHelperMessageReceiver := broadcastchan.Receiver[*gws.Message]{
		DataChan: helper.MessageChan,
		QuitChan: make(chan struct{}),
	}
	wsClientReceiver := broadcastchan.Receiver[*gws.Message]{
		DataChan: make(chan *gws.Message),
		QuitChan: make(chan struct{}),
	}
	messageBroadcastChan := broadcastchan.NewBroadcastGroup(
		make(chan *gws.Message),
		[]*broadcastchan.Receiver[*gws.Message]{
			&wsClientReceiver,
			&runnerHelperMessageReceiver,
		},
	)
	var handler gws.Event = &WsClientHandler{
		OnOpenHandler: func(socket *gws.Conn) {
			utillog.PrintfTiming("WebSocket client connected to server\n")
			helper.conn = socket
			go runner.Run(&helper)
		},
		OnMessageHandler: func(socket *gws.Conn, message *gws.Message) {
			utillog.PrintfTiming("WebSocket client received message\n")
			messageBroadcastChan.GroupInChan <- message
		},
	}

	// Dial the WebSocket server
	conn, _, err := gws.NewClient(handler, &gws.ClientOption{
		Addr: serverURL,
	})
	if utilerror.LogError("Failed to connect to WebSocket server: %v\n", err) {
		return err
	}

	utilerror.FatalError("Failed to create WebSocket client: %v\n", err)
	done := make(chan struct{})
	go func() {
		conn.ReadLoop()
		close(done)
	}()

	select {
	case <-done:
		t.Logf("WebSocket client read loop completed\n")
	case <-time.After(1 * time.Second):
		conn.NetConn().Close()
	}

	return nil
}
