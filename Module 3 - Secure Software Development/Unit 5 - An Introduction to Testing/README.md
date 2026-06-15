# Unit 5: An Introduction to Testing

This unit focuses on two core aspects of software quality: **code complexity** and **automated testing**. Together, these activities explore how code can be evaluated and improved, both through human reflection on AI-assisted development and through hands-on use of Python's `unittest` framework.

## Contents

### 1. [Code Complexity Reflection](code-complexity.md)

A reflective activity examining what code complexity is, how it is measured (lines of code, maintainability index, cyclomatic complexity, rework ratio, Halstead volume), and how AI tools such as ChatGPT can support — and sometimes complicate — efforts to reduce it. Includes reflections on two academic papers covering AI-assisted code refinement and the quality of AI-generated code.

### 2. [Unit Testing Activity](unit-testing.md)

A practical activity applying Python's `unittest` framework to an existing piece of code (a deck-of-cards shuffler). Covers the key concepts of unit, functional/integration, and regression testing, the building blocks of `unittest` (fixtures, cases, suites, runners), and includes a refactored version of the source code (`cards.py`) alongside a full test suite (`test_cards.py`).

## Key Themes Across This Unit

- **Complexity and testability are linked.** Code that is broken into small, single-purpose functions is both easier to understand and easier to test — as shown in the refactoring of the card-shuffling script.
- **Automation reduces risk.** Whether using AI tools to assist with code refinement or using `unittest` to automatically verify behaviour, automation provides a faster and more repeatable way of catching issues than manual checking alone.
- **Human oversight remains essential.** AI-assisted suggestions and automated test results both need to be interpreted by a developer who understands the wider context of the code — automation supports good practice but does not replace it.

## Files in This Unit

| File | Description |
|------|-------------|
| `unit-5-code-complexity.md` | Reflection on code complexity and AI-assisted refinement |
| `unit-5-unit-testing.md` | Unit testing activity write-up |
| `cards.py` | Refactored deck-shuffling code |
| `test_cards.py` | Unit tests for `cards.py` |
