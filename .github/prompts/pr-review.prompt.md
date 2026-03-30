# PR Review Prompt

Task:
Review all changes in the current branch against main.

Focus Areas:
1. Architecture boundary violations (Route -> Service -> Repository)
2. Functional regressions and edge-case bugs
3. Missing validation and exception mapping
4. Security and secret-handling issues
5. Test gaps and brittle assertions
6. Frontend loading/error handling and typing issues

Output Format:
- BLOCKER: must fix before merge
- WARNING: should fix in this PR
- SUGGESTION: optional improvement

For each finding include:
- Severity
- File path
- Line reference
- Risk summary
- Concrete fix recommendation

End with PASS or NEEDS WORK.
