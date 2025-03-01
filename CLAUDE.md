# Project Overview

"speaker-be" is a language learning application focused on vocabulary acquisition and translation. 

## Key Features
- AI-powered translations and definitions using ChatGPT models
- Word breakdown with detailed definitions, examples, and etymology
- Flashcard system with decks for vocabulary practice
- Multi-language support with language selection
- Custom card configurations for personalized learning

## Architecture
- Backend: Go-based API with OpenAI integration
- Frontend: Vue 3 application with TypeScript
- Databases:
  - PostgreSQL (DEPRECATED)
  - Neo4j graph database (DEPRECATED)
  - SurrealDB (DEPRECATED)
  - Cassandra (PLANNED as future database solution)
- Type Sharing: JSON Schema for cross-service type definitions

## Project Structure
- `/api-go`: Go backend API and AI processing
- `/vue`: Vue 3 frontend
- `/json-schema`: Shared type definitions
- `/migrations`: Database migration files
- `/scripts`: Build and utility scripts

# Development Commands

## Backend (api-go)
- `cd api-go && go test ./...` - Run all Go tests
- `go test -run TestCardGenerator ./api-go/test/e2etest_test/cardgen` - Run specific Go test

## Frontend (vue)
- `cd vue && yarn dev` - Start Vue development server
- `cd vue && yarn build` - Build Vue frontend
- `cd vue && yarn lint` - Lint Vue code
- `cd vue && yarn test` - Run Vue tests
- `cd vue && yarn test --test=<TestName>` - Run specific Vue test

## Shared Types (json-schema)
- `./scripts/generate-json-schema.sh` - Generate schemas across services
- `./scripts/watch-json-schema.sh` - Watch and rebuild schemas on changes

# Code Style Guidelines

## Go
- Use PascalCase for public functions/types, lowercase for package names
- Error handling with explicit checks and early returns
- Organize imports: standard library first, then third-party, then local

## TypeScript/Vue
- Use TypeScript's strict mode with proper typing
- Vue 3 Composition API with `<script setup>` pattern
- Use camelCase for functions/variables, PascalCase for components
- Follow consistent error handling patterns

# Database Plan
- Current databases (PostgreSQL, Neo4j, SurrealDB) are deprecated
- Future plans involve using Cassandra as a database solution
- Current data modeling is outdated and subject to redesign