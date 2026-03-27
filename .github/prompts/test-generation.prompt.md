# Test Generation Skill

When this skill is invoked, always:

1. Read the source file(s) being tested before writing any test.
2. Identify: the layer (repository/service/router/component),
   all public methods or endpoints, all possible outcomes
   (success, not found, invalid input, duplicate, etc.).
3. Generate tests for EVERY public method and EVERY outcome.
4. Follow naming: `test_<what>_when_<condition>` (Python),
   `should <do something> when <condition>` (React).
5. Structure every test as Arrange / Act / Assert with a blank
   line separating each section.
6. For repository tests: use real SQLite session from conftest.
7. For service tests: mock repository with MagicMock, verify
   repository method calls with `assert_called_once_with`.
8. For router tests: use TestClient, override `get_db` dependency,
   test status codes AND response body shape.
9. For React component tests: mock API module with `vi.mock()`,
   test each visual state (loading, error, empty, populated).
10. Never test implementation details — test observable behaviour.
11. Add a one-line docstring to every test function explaining
    what it verifies.
12. Generate conftest.py fixtures if they don't already exist.
