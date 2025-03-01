# Vocabo: Offline-First Language Learning Mobile App

## Project Overview

Vocabo is a cross-platform mobile application focused on language learning and vocabulary acquisition. It's designed with an offline-first approach to ensure functionality without internet connectivity, while supporting future synchronization capabilities.

## Key Features

- **Offline-First Architecture**: Works fully without internet connectivity
- **Local SQLite Database**: Fast local storage for vocabulary and learning data
- **Offline LLM Integration**: Supports word translation and definitions without internet
- **Cross-Platform Support**: Built with Flutter for iOS and Android compatibility
- **Batch Synchronization**: Future support for syncing with self-hosted or cloud services
- **Small Nation Language Support**: Specialized in supporting less common languages

## Technical Architecture

### Core Components

1. **UI Layer (React Native, Expo)**

   - Minimal UI for testing and debugging in Phase 1
   - Material Design 3 with customizable theming in later phases
   - Responsive design for various device sizes

2. **Application Layer**

   - State management
   - Business logic and use cases
   - Navigation system

3. **Data Layer**

   - Local SQLite database via `sqflite` package
   - Repository pattern implementation
   - Entity models and data transfer objects

4. **LLM Integration**

   - Local model hosting (DeepSeek, Phi-4, Qwen, or Gemma)
   - Optimized for vocabulary translation and definitions
   - Model management and updates

5. **Synchronization Module (Future)**
   - Batch sync with remote servers
   - Conflict resolution strategies
   - Compatibility with Cassandra for server-side storage

## Development Roadmap

### Phase 1: LLM Testing Foundation (Current)

- Basic project setup and architecture
- Minimal UI suitable for debugging purposes
- Local LLM integration with hard-coded tasks
- Performance testing and optimization of LLM models
- Basic SQLite implementation for test results storage

### Phase 2: Core Functionality

- Expanded UI components and navigation
- Complete SQLite database implementation
- Vocabulary management features
- Enhanced LLM integration with user inputs

### Phase 3: Advanced Features

- Flashcard and learning systems
- User profiles and progress tracking
- Analytics and learning optimization

### Phase 4: Synchronization

- Implement batch synchronization
- Self-hosted server options
- Cloud synchronization services

## Project Success Criteria

1. **Performance**: Fast response times even on older devices
2. **Offline Capability**: 100% functionality without internet
3. **Battery Efficiency**: Minimal impact on device battery
4. **Storage Optimization**: Efficient use of device storage
5. **User Experience**: Intuitive and accessible design

## Technical Decisions

- **Flutter**: Selected for cross-platform capabilities and performance
- **SQLite**: Chosen for reliable local data storage with SQL capabilities
- **Local LLMs**: Selected lightweight models optimized for mobile devices
- **JSON Schema**: Used for consistent data modeling across components

## Testing Strategy

- Unit tests for business logic
- Integration tests for data flow
- UI tests for critical user journeys
- Performance benchmarks for optimization

## Deployment Strategy

- CI/CD pipeline for automated testing and releases
- Beta testing program for early feedback
- Phased rollout strategy for app store deployments

## Phase 1 Milestones

1. **Project Setup**

   - Flutter project initialization
   - Architecture implementation
   - Dependencies configuration

2. **LLM Integration**

   - Research and select appropriate lightweight LLM
   - Implement model loading and initialization
   - Create service layer for LLM interaction

3. **Testing Framework**

   - Create minimal debug UI for testing LLMs
   - Implement hard-coded test cases for translation tasks
   - Build performance measurement tools

4. **Evaluation**
   - Test various models for performance/accuracy tradeoffs
   - Measure memory usage and battery impact
   - Document results and select optimal model configuration
