package config

import (
	"log"

	"github.com/caarlos0/env/v10"
)

// Load loads the configuration from environment variables
func (c *Config) Load() error {
	if err := env.Parse(c); err != nil {
		return err
	}
	return nil
}

// MustLoad loads the configuration or panics
func MustLoad() *Config {
	cfg := &Config{}
	if err := cfg.Load(); err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}
	return cfg
}
