package neo4jdb

import (
	"api-go/pkg/utilerror"
	"context"
	"sync"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

var Driver neo4j.DriverWithContext

func Init(ctx context.Context, waitGroup *sync.WaitGroup) {
	var err error
	Driver, err = neo4j.NewDriverWithContext("bolt://localhost:7687", neo4j.BasicAuth("neo4j", "devlocal", ""))
	utilerror.FatalError("Unable to create driver", err)
	err = Driver.VerifyConnectivity(ctx)
	utilerror.FatalError("Unable to connect to database", err)

	<-ctx.Done()
	{
		utilerror.LogError("Context cancelled", ctx.Err())
		err = Driver.Close(ctx)
		utilerror.LogError("Database connection closed", err)
		waitGroup.Done()
	}
}

func ExecuteQuery(query string, params map[string]any) (*neo4j.EagerResult, error) {
	ctx := context.Background()
	result, err := neo4j.ExecuteQuery(ctx, Driver,
		query,
		params, neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"))
	utilerror.LogError("Error executing query", err)
	return result, err
}
