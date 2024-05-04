package httpapp

import (
	"api-go/pkg/apimessagehandler"
	"api-go/pkg/config"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"fmt"
	"io"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func Init() {
	echoApp := echo.New()
	echoApp.Use(middleware.CORS())
	echoApp.POST("/message", func(ctx echo.Context) error {
		echoApp.Logger.Debug("Received message")
		// userInfo, err := pgdb.Queries.GetUserInfo(ctx.Request().Context(), "admin")
		// utilerror.LogError("Failed to get user info", err)
		// log.Printf("User info: %v", userInfo)
		var message = genjsonschema.MessageBaseInput{}
		body, err := io.ReadAll(ctx.Request().Body)
		if utilerror.LogError("Failed to read body", err) {
			return ctx.JSON(400, "Failed to read body")
		}
		err = message.UnmarshalJSON(body)
		if utilerror.LogError("Failed to parse body json", err) {
			return ctx.JSON(400, "Failed to parse body json")
		}

		output := apimessagehandler.HandleMessage(message)
		status := 500
		if len(output.Errors) == 0 {
			status = 200
		}

		return ctx.JSON(status, map[string]interface{}{
			"output": output,
		})
	})
	echoApp.Logger.Fatal(echoApp.Start(fmt.Sprintf(":%s", config.Config.HttpPort)))
}
