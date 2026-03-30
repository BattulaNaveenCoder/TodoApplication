# PR Review Prompt

Review the current branch as a pre-merge quality gate.

## Review Priorities
1. Correctness and regressions
2. Architecture compliance
3. Security concerns
4. Test completeness
5. Maintainability

## Required Checks
- Router -> Service -> Repository layering is respected.
- No business logic in routers.
- No direct DB access in services.
- Errors are meaningful and structured.
- New/changed logic includes tests.

## Output Format
1. Summary verdict: PASS or NEEDS WORK
2. Findings grouped by severity: CRITICAL, HIGH, MEDIUM, LOW
3. For each finding: file, line, issue, impact, fix recommendation
4. Residual risks and missing test coverage
