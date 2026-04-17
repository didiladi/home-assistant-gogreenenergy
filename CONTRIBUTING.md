# Contributing to GoGreenEnergy Integration

First off, thank you for considering contributing to the GoGreenEnergy integration for Home Assistant! It's people like you that make Home Assistant such a great platform.

## Getting Started

1. Fork this repository.
2. Clone your fork locally.
3. Add the `custom_components/gogreenenergy` directory to your local Home Assistant testing environment.
4. Create a new branch for your feature or bugfix.

## Development Guidelines

- **Code Style:** We follow standard Python code styling conventions (PEP 8). We strongly recommend using `black` for formatting and `flake8` for linting.
- **Home Assistant Standards:** Ensure your code aligns with the official Home Assistant developer documentation and guidelines. Avoid synchronous blocking calls in asynchronous functions.
- **Testing:** Make sure any new logic is tested. (Note: A testing framework setup might be pending, but please test the changes on a live Home Assistant instance before submitting a PR).

## Submitting a Pull Request

1. Make sure your code is clean and functional.
2. Commit your changes with descriptive commit messages.
3. Push your branch to your GitHub fork.
4. Open a Pull Request (PR) against the `main` branch of this repository.
5. In your PR description, clearly describe what the changes do and any testing you performed.

## Reporting Bugs

If you find a bug, please create an Issue on GitHub. Include:
- Your Home Assistant version.
- The version of this integration you are using.
- Relevant logs and configuration snippets.
- Steps to reproduce the bug.

## Feature Requests

Have a great idea? Open an Issue on GitHub and use the title prefix `[Feature Request]`. We'd love to hear it!
