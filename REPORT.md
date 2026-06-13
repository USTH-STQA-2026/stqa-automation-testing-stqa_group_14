# Software Testing Project Report

## Automation Testing Framework for Flutter Web CanvasKit Library Book Borrowing System

## 1. Executive Summary

This project presents a completed automation testing framework for the Library Book Borrowing System hosted at `https://stqa.rbc.vn`. The system supports digital library operations such as member authentication, book search, borrowing, returning, overdue handling, member administration, and bilingual user interaction.

The automation framework was developed using Python, Pytest, Playwright, and Flutter Accessibility Semantics. It performs end-to-end browser-based testing against a Flutter Web CanvasKit application. Since CanvasKit renders the visual interface primarily through a canvas instead of standard HTML elements, the framework uses the Flutter Accessibility Semantics Tree to locate and interact with application controls.

The project demonstrates a practical software testing solution for a modern web application whose interface cannot be automated reliably through ordinary DOM selectors alone. The test suite validates core business workflows, extended role-based scenarios, and evidence collection through automated screenshots and structured test execution.

## 2. Introduction

Software testing is a key activity in verifying that a system satisfies functional requirements and supports expected user workflows. In this project, automated UI testing is applied to a Library Book Borrowing System used for Software Testing and Quality Assurance coursework.

The tested application is implemented with Flutter Web using the CanvasKit renderer. This introduces a specific automation challenge: most visible UI elements are drawn on a canvas, so they are not exposed as ordinary HTML buttons, inputs, or tables. To address this, the framework enables and uses Flutter Accessibility Semantics, which creates semantic nodes such as `flt-semantics`, ARIA labels, roles, text fields, buttons, tabs, and groups.

The result is a reusable automation framework that allows testers to execute consistent end-to-end validation of the system from the perspective of real users.

## 3. Project Objectives

The project was created with the following objectives:

| Objective | Description |
|---|---|
| Automate functional UI testing | Execute browser-based tests for major user workflows without manual repetition. |
| Validate business requirements | Confirm that library operations follow the SRS and BRD expectations. |
| Support multiple user roles | Test both member and librarian workflows. |
| Adapt automation to Flutter Web CanvasKit | Use Accessibility Semantics Tree interaction for a canvas-rendered interface. |
| Provide reusable test infrastructure | Centralize login, browser setup, waiting logic, screenshots, and UI helpers. |
| Collect test evidence | Capture screenshots and console output to support evaluation and demonstration. |
| Demonstrate academic testing practice | Present a complete testing deliverable suitable for lecturer and project evaluation. |

## 4. System Under Test

The System Under Test is the Library Book Borrowing System deployed at:

```text
https://stqa.rbc.vn
```

The system provides a web-based interface for managing a small library operation.

| User Role | Main Capabilities |
|---|---|
| Member | Log in, view books, search books, filter by category, borrow eligible books, return personal borrowed books, and view borrow records. |
| Librarian | Log in, view books, manage members, review borrowing records, and perform administrative workflows. |

The system supports Vietnamese and English interfaces, enabling bilingual workflow validation.

## 5. Testing Scope

The testing scope focuses on end-to-end functional UI automation.

| Area | Scope Included |
|---|---|
| Authentication | Valid login, invalid login, missing credentials, librarian login, logout. |
| Book catalog | Book visibility, title search, author search, category filtering. |
| Borrow workflow | Borrowing available books, confirmation dialog interaction, borrow record creation, due-date validation. |
| Return workflow | Returning borrowed books, returned status verification, book availability update. |
| Member eligibility | Borrowing behavior for active, suspended, expired, and limit-reached member states. |
| Member management | Librarian member creation, email validation, duplicate email handling. |
| Borrow records | Personal records, lookup behavior, ownership-based interaction. |
| Overdue handling | Due-date boundary and overdue return workflows. |
| Bilingual UI | Switching the interface from Vietnamese to English. |
| Evidence collection | Automatic screenshot capture for completed test outcomes. |

The scope is centered on automated functional validation and does not include source code review or code quality evaluation.

## 6. Testing Strategy

The project uses an end-to-end black-box UI testing strategy. Tests interact with the deployed web application through a browser in the same way a user would interact with it.

The strategy consists of:

| Strategy Element | Implementation |
|---|---|
| Test runner | Pytest discovers and executes test functions. |
| Browser automation | Playwright controls Chromium. |
| UI interaction | Flutter Accessibility Semantics Tree is used for fields, buttons, tabs, and records. |
| Test isolation | Each test receives a fresh browser context. |
| Test data | Seed data and configurable accounts are used through `.env`. |
| Assertions | Tests verify visible text, ARIA labels, statuses, records, and access behavior. |
| Evidence | Screenshots are captured automatically after test execution. |

The strategy is designed to make tests repeatable, readable, and aligned with user-facing requirements.

## 7. Automation Framework Architecture

The automation framework is organized around Pytest fixtures, Playwright browser control, and Flutter-specific helper functions.

```text
+-----------------------------+
|        Pytest Test Suite     |
+-------------+---------------+
              |
              v
+-----------------------------+
|       Shared Fixtures        |
|  browser, page, test_config  |
+-------------+---------------+
              |
              v
+-----------------------------+
|       Playwright Driver      |
+-------------+---------------+
              |
              v
+-----------------------------+
|       Chromium Browser       |
+-------------+---------------+
              |
              v
+-----------------------------+
| Flutter Web CanvasKit App    |
+-------------+---------------+
              |
              v
+-----------------------------+
| Accessibility Semantics Tree |
| flt-semantics, aria-labels   |
+-----------------------------+
```

The framework does not depend on conventional DOM structure for the Flutter interface. Instead, it enables semantics and then uses semantic locators to perform actions and validations.

## 8. Technology Stack

| Layer | Technology |
|---|---|
| Programming language | Python |
| Test runner | Pytest |
| Browser automation | Playwright |
| Browser engine | Chromium |
| Configuration loading | python-dotenv |
| Application renderer | Flutter Web CanvasKit |
| Interaction layer | Flutter Accessibility Semantics Tree |
| Documentation | Markdown |

Project dependencies are managed in `requirements.txt`:

```text
playwright==1.49.1
pytest==8.3.4
pytest-playwright==0.6.2
python-dotenv==1.1.0
```

## 9. Framework Components and Responsibilities

| Component | Responsibility |
|---|---|
| `tests/test_login.py` | Authentication scenarios for member and librarian accounts. |
| `tests/test_search.py` | Book search, author search, category filtering, and case-insensitive behavior. |
| `tests/test_borrow_return.py` | Borrowing, borrow records, returning, borrow limits, and member eligibility workflows. |
| `tests/test_general.py` | Logout and language switching workflows. |
| `tests/test_bonus.py` | Extended scenarios for overdue handling, member management, role access, and ownership behavior. |
| `conftest.py` | Shared fixtures, browser setup, environment loading, Flutter helpers, login utilities, waits, and screenshots. |
| `web_detector.py` | Web technology detection and technology-aware interaction support. |
| `.env` / `.env.example` | Runtime configuration for target URL and test accounts. |
| `screenshots/` | Stores visual evidence from test execution. |
| `docs/` | Stores SRS, BRD, assignment guide, test accounts, and supporting documentation. |
| `pytest.ini` | Defines Pytest discovery path and default execution options. |

The framework centralizes repeated operations in helper functions so that individual test cases remain focused on business behavior.

## 10. Test Execution Workflow

The typical execution process is:

```text
1. Install dependencies
        |
        v
2. Install Playwright Chromium
        |
        v
3. Configure .env test accounts
        |
        v
4. Run pytest
        |
        v
5. Launch Chromium with accessibility support
        |
        v
6. Open application URL
        |
        v
7. Enable Flutter Semantics Tree
        |
        v
8. Execute test workflow
        |
        v
9. Perform assertions
        |
        v
10. Capture screenshot evidence
```

Common execution commands:

```bash
pip install -r requirements.txt
playwright install chromium
pytest -v
```

The Pytest configuration uses verbose output and short tracebacks:

```ini
[pytest]
testpaths = tests
addopts = -v --tb=short
```

## 11. Test Scenarios Covered

The implemented suite contains 28 automated test functions across five test modules.

| Test Area | Scenarios |
|---|---|
| Authentication | Successful member login, successful librarian login, wrong password, unknown email, empty fields, missing email, missing password. |
| Search and filter | Search by title, no-result search, filter by category, search by author, case-insensitive title search, case-insensitive category filter. |
| Borrowing | Borrow available book, confirm borrow dialog, validate borrowed status, validate borrow record, validate due date. |
| Borrow rules | Enforce borrow limit, reject suspended member borrowing, reject expired member borrowing. |
| Returning | Return borrowed book, verify returned status, verify book availability after return. |
| Borrow records | View personal borrowed books, verify record ownership behavior. |
| Overdue workflows | Return on due-date boundary, return overdue borrowed book. |
| Member management | Add valid member, reject email without domain dot, reject email without `@`, reject duplicate email. |
| Role access | Verify normal member cannot access the Members tab. |
| General UI | Logout and switch language to English. |

## 12. Test Coverage Summary

| File | Number of Tests | Main Coverage |
|---|---:|---|
| `tests/test_login.py` | 7 | Login success and validation scenarios. |
| `tests/test_search.py` | 6 | Book search and filtering. |
| `tests/test_borrow_return.py` | 6 | Borrowing, returning, limits, and eligibility. |
| `tests/test_general.py` | 2 | Logout and language switching. |
| `tests/test_bonus.py` | 8 | Overdue handling, member management, role access, and record ownership. |
| **Total** | **28** | **Core and extended functional workflows.** |

Requirement alignment:

| Requirement Area | Automation Coverage |
|---|---|
| Login | Member and librarian login, invalid credential handling, required-field behavior. |
| View book list | Catalog interactions through search, filtering, borrow, and return workflows. |
| Search and filter | Title search, author search, category filter, case-insensitive behavior. |
| Borrow book | Successful borrow, borrow record creation, due-date calculation, eligibility rules. |
| Return book | Successful return, returned status, book availability update. |
| Overdue handling | Due-date boundary return and overdue return. |
| Member management | Member creation, email validation, duplicate email handling, role-based access. |
| Borrow record lookup | Personal records and ownership-based return behavior. |

## 13. Test Data Management

The project uses deterministic seed data provided by the application and configurable test accounts from environment variables.

| Data Type | Management Approach |
|---|---|
| Target URL | Configured through `BASE_URL`. |
| Default member account | Configured through `TEST_EMAIL`, `TEST_PASSWORD`, and `TEST_DISPLAY_NAME`. |
| Librarian account | Configured through `LIBRARIAN_EMAIL` and `LIBRARIAN_PASSWORD`, or documented seed credentials. |
| Additional member account | Configured through `MEMBER_OTHER_EMAIL` and `MEMBER_OTHER_PASSWORD`. |
| Suspended member account | Configured through `SUSPENDED_EMAIL` and `SUSPENDED_PASSWORD`. |
| Expired member account | Configured through `EXPIRED_EMAIL` and `EXPIRED_PASSWORD`. |
| Application data | Stored in browser memory and restored through fresh test contexts. |

Each test receives an isolated Playwright browser context. This allows tests to execute from a controlled application state and supports repeatable demonstrations.

## 14. Reporting and Evidence Collection

The framework provides evidence through automated screenshots and Pytest console output.

| Reporting Mechanism | Description |
|---|---|
| Pytest verbose output | Displays executed tests and test status. |
| Short traceback mode | Keeps test output concise and readable. |
| Automatic screenshot capture | Captures a full-page screenshot after each test. |
| Pass screenshots | Stored in `screenshots/pass/`. |
| Evidence screenshots for failed outcomes | Stored in `screenshots/bug/`. |
| Console messages | Used for technology detection output and screenshot capture information. |

Screenshot filenames are generated from test identifiers so that evidence can be matched to the corresponding scenario.

## 15. Challenges Encountered

The project involved several testing challenges related to the application technology and workflow characteristics.

| Challenge | Explanation |
|---|---|
| Canvas-rendered UI | Flutter Web CanvasKit draws most visual elements on a canvas, so normal HTML selectors are not sufficient for direct UI automation. |
| Semantic interaction requirement | The framework needs to enable Flutter Accessibility Semantics before fields, buttons, tabs, and book records become accessible to automation. |
| Asynchronous Flutter rendering | UI state and semantics nodes may update after user actions, requiring smart waiting logic. |
| Bilingual interface | Tests need to handle Vietnamese labels and verify English text after language switching. |
| Role-specific behavior | Member and librarian accounts expose different tabs and workflows. |
| Test state control | Borrowing and returning operations change visible application state during execution. |

These challenges shaped the framework design and led to a specialized automation approach for Flutter Web.

## 16. Solutions Implemented

The framework implements several solutions to support reliable end-to-end testing.

| Solution | Implementation |
|---|---|
| Flutter Semantics enablement | `enable_flutter_semantics()` activates semantic nodes for automation. |
| Semantic field interaction | `flutter_fill()` fills inputs using ARIA labels and Flutter text editing hosts. |
| Semantic button interaction | `flutter_click_button()` clicks buttons through `flt-semantics` role and visible text. |
| Smart waiting | `wait_for_flutter()` waits for text, selectors, or semantics nodes to appear. |
| Shared login workflow | `login()` centralizes navigation, credential input, submit action, and post-login waiting. |
| Browser context isolation | The `page` fixture creates a new context for each test. |
| Environment-driven accounts | `.env` allows flexible account and URL configuration. |
| Automatic evidence capture | An autouse Pytest fixture saves screenshots after test execution. |
| Technology detection | `web_detector.py` identifies Flutter CanvasKit and supports technology-aware interaction. |

These solutions make the framework reusable across test files and maintain a clear separation between test scenarios and technical interaction details.

## 17. Results and Achievements

The project produced a complete automation testing framework for a Flutter Web CanvasKit application.

Key achievements include:

| Achievement | Description |
|---|---|
| Completed end-to-end workflow automation | The suite automates login, search, borrow, return, member management, overdue handling, and language switching. |
| Flutter-aware interaction model | The framework successfully uses Accessibility Semantics Tree interaction for a canvas-rendered application. |
| Reusable framework utilities | Common browser setup, login, wait, click, fill, and screenshot operations are centralized. |
| Structured test organization | Test cases are grouped by functional area and user workflow. |
| Configurable execution | Environment variables support different accounts and execution environments. |
| Evidence-based testing | Screenshots are collected automatically for review and presentation. |
| Requirement-oriented coverage | Test scenarios are aligned with major SRS requirement areas. |

The final suite contains 28 automated test functions covering both required assignment scenarios and extended business workflows.

## 18. Conclusion

This project successfully delivers an automation testing framework for the Library Book Borrowing System. The framework demonstrates how Pytest and Playwright can be adapted for a Flutter Web CanvasKit application by using the Flutter Accessibility Semantics Tree as the primary interaction layer.

From a software testing perspective, the project verifies important library workflows across member and librarian roles, validates business rules through end-to-end scenarios, and provides screenshot evidence for evaluation. The framework is organized around reusable fixtures and helper functions, making the test suite structured, repeatable, and suitable for academic demonstration.

The completed work represents a practical automated testing deliverable for a modern web application with non-standard rendering behavior.

## 19. Future Enhancements

Future development may extend the existing framework in the following directions:

| Enhancement | Expected Value |
|---|---|
| Continuous integration execution | Run the test suite automatically on repository updates and preserve artifacts. |
| HTML test dashboard | Present test results, screenshots, and requirement mapping in a visual report. |
| Browser matrix execution | Demonstrate behavior across additional supported browser engines. |
| Parameterized test data | Execute more account, book, category, and record combinations. |
| Performance checkpoints | Record key workflow timings such as login, search, borrow, and return. |
| Presentation package | Prepare selected screenshots and coverage tables for project demonstration. |

