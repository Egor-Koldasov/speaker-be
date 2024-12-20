package wsapp

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/router"
	"api-go/pkg/utiljson"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/lxzan/gws"
	"github.com/xeipuuv/gojsonschema"
)

const (
	PingInterval = 5 * time.Second
	PingWait     = 10 * time.Second
)

func Init() {
	upgrader := gws.NewUpgrader(&Handler{}, &gws.ServerOption{
		ParallelEnabled:   true,                                 // Parallel message processing
		Recovery:          gws.Recovery,                         // Exception recovery
		PermessageDeflate: gws.PermessageDeflate{Enabled: true}, // Enable compression
	})
	http.HandleFunc("/ws", func(writer http.ResponseWriter, request *http.Request) {
		fmt.Printf("Connect\n")
		socket, err := upgrader.Upgrade(writer, request)
		if err != nil {
			return
		}
		go func() {
			socket.ReadLoop() // Blocking prevents the context from being GC.
		}()
	})
	fmt.Printf("Starting WS server on :6969\n")
	http.ListenAndServe(":6969", nil)
}

type Handler struct{}

func (c *Handler) OnOpen(socket *gws.Conn) {
	_ = socket.SetDeadline(time.Now().Add(PingInterval + PingWait))
}

func (c *Handler) OnClose(socket *gws.Conn, err error) {}

func (c *Handler) OnPing(socket *gws.Conn, payload []byte) {
	_ = socket.SetDeadline(time.Now().Add(PingInterval + PingWait))
	_ = socket.WritePong(nil)
}

func (c *Handler) OnPong(socket *gws.Conn, payload []byte) {}

func (c *Handler) OnMessage(socket *gws.Conn, message *gws.Message) {
	defer message.Close()

	buffer := message.Bytes()

	messageBufferLoader := gojsonschema.NewBytesLoader(buffer)

	appErrors := jsonvalidate.ValidateJson(jsonvalidate.SchemaPathWsMessageBase, messageBufferLoader, genjsonschema.ErrorNameInternal)

	log.Printf("Errors: %v\n", appErrors)

	if len(*appErrors) > 0 {
		return
	}
	messageStruct := utiljson.ParseJson[genjsonschema.WsMessageBase](string(buffer[:]))

	fmt.Printf("Received message: %v\n", messageStruct)

	response := router.HandleWsMessage(&messageStruct)

	buffer = []byte(utiljson.Marshal(response))

	socket.WriteMessage(message.Opcode, buffer)
}
