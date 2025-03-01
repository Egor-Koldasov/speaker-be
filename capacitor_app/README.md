# Vocabo - Offline LLM Language Learning App

A cross-platform mobile application focused on language learning using offline-first architecture with local LLM capabilities.

## Project Overview

Vocabo is designed to provide language learning tools without requiring an internet connection. The app uses local LLMs to perform translation, word definition, and language learning tasks directly on the device.

See the [full project documentation](docs/PROJECT.md) for detailed design and architecture information.

## Phase 1 Focus: LLM Testing

The current phase focuses on:
- Testing various local LLM models for performance and accuracy
- Evaluating language translation capabilities
- Building the core architecture for offline operation
- Implementing a minimal UI for debugging and testing

## Setup Instructions

### Prerequisites

- Flutter SDK (latest stable version)
- Android Studio / Xcode for device deployment
- 2GB+ of free storage for LLM models

### Installation

1. Clone the repository
```bash
git clone https://your-repository-url/vocabo.git
cd vocabo
```

2. Install dependencies
```bash
flutter pub get
```

3. Generate code (for freezed models)
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

4. Run the app
```bash
flutter run
```

## Testing LLM Models

The application provides a simple UI for testing different local LLM models against predefined language tasks:

1. Choose a test case (e.g., English to Spanish translation)
2. Select an LLM model to test
3. Run the test to see results and performance metrics
4. Compare models for speed and accuracy

## Future Development

After Phase 1 (LLM testing), the project will progress to:
- Phase 2: Core Functionality - full vocabulary management and enhanced UI
- Phase 3: Advanced Features - flashcards, user profiles, analytics
- Phase 4: Synchronization - optional cloud/self-hosted sync capabilities

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
