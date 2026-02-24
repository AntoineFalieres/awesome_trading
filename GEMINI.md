# Constitution for the awesome-trading Project

This document defines the identity, knowledge, and rules of engagement for the Gemini agent operating within this repository. All actions must strictly adhere to these principles.

---

## 1. Project Context & Core Purpose

**Project Overview:** This project is a Python package that aims to calculate the right point point to trade stocks or crypto.

**Architecture:**
*   **Python Package:** This is a standard Python package, installable via `uv`.

**Technology Stack:**
*   **Language:** Python 3
*   **Packaging:** `setuptools`

---

## 2. Key Documents & Source of Truth

You MUST refer to the following files as the canonical source of truth for project information.

*   **Available Rules & Usage:** The `README.md` file contains the definitive list of all rules, their purpose, and instructions for use.
*   **Package Dependencies & Metadata:** The `setup.py` file is the source of truth for package name, version, author, and dependencies.

---

## 3. Coding Standards & Design Patterns

**Quality Gates:**
*   All Python code MUST strictly adhere to the **PEP8 style guide**.
*   All new rules MUST be documented in the `README.md`.

---

## 4. Standardizing Workflows

**Common Commands:**
*   **Install for development:** `pip install -e .`
*   **Run tests:** `pytest`

**Workflow: Adding a New Rule**
1.  **Update the README:** Add a new entry to the appropriate table in `README.md` to document the new rule.
2.  **Verify:** Propose running `pytest` to ensure the changes haven't introduced any regressions.

---

## 5. Behavioral Guardrails

**Prohibited Actions:**
*   **NEVER** add new third-party dependencies to `install_requires` in `setup.py` without explicit approval. This package must remain lightweight.
*   **DO NOT** modify the package version in `setup.py` unless specifically instructed to do so as part of a release.
*   **NEVER** add rules that are specific to a single, niche dbt project.

---

## 6. Interaction Style & Tool Usage

**Interaction Style: Planning First**
*   For any request that involves creating or modifying rules, you **MUST** first present a step-by-step plan that follows the workflow defined in Section 4.
*   Do not proceed with execution until I explicitly approve the plan.

**Tool Preferences:**
*   When updating the `README.md`, always read the entire file first. Provide the complete, updated content to the `replace` tool to avoid corrupting the Markdown tables.