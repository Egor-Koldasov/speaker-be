package pgdb

import (
	"api-go/pkg/config"
	"api-go/pkg/sqlgen"
	"api-go/pkg/utilerror"
	"context"
	"sync"

	"github.com/jackc/pgx/v5"
)

var Conn *pgx.Conn
var Queries *sqlgen.Queries

func Init(ctx context.Context, waitGroup *sync.WaitGroup) {
	var err error

	Conn, err = pgx.Connect(ctx, config.Config.PgConnectionString)
	utilerror.FatalError("Unable to connect to database", err)

	Queries = sqlgen.New(Conn)

	<-ctx.Done()
	{
		utilerror.LogError("Context cancelled", ctx.Err())
		err = Conn.Close(ctx)
		utilerror.LogError("Database connection closed", err)
		waitGroup.Done()
	}

}
