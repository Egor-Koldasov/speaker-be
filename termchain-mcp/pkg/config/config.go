package config

// Config holds all configuration for the application
type Config struct {
	Server struct {
		Port string `env:"PORT" envDefault:"8082"`
	}
}

// NewConfig creates a new Config instance with default values
func NewConfig() *Config {
	cfg := &Config{}
	// The default port is set via the struct tag and will be used automatically
	return cfg
}
