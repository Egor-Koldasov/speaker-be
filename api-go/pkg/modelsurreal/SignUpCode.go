package modelsurreal

type SignUpCode struct {
	ModelSurrealBase
	Email string
	Code  string
}
