# Security Review Skill

When this skill is invoked, always:

1. Read all files changed in the current feature branch.
2. Produce a structured report with sections:

   **CRITICAL — must fix before merge:**
   - Any raw SQL string concatenation (SQL injection risk)
   - Credentials, API keys, or secrets in source code
   - Stack traces or internal error details exposed in API responses
   - .env file committed to git

   **HIGH — should fix before merge:**
   - Inputs accepted without Pydantic validation
   - Missing error handling on DB operations
   - CORS configured to allow all origins (*)
   - Unhandled exceptions that could crash the server

   **MEDIUM — address in next sprint:**
   - Missing rate limiting on write endpoints
   - No input length limits on string fields
   - Console.log statements left in frontend production code

   **LOW — best practice suggestions:**
   - Functions longer than 40 lines
   - Missing docstrings on public functions
   - Test coverage below 80% on any module

3. For each finding report: severity, file, line number,
   description of risk, specific recommended fix.
4. End report with a **PASS** or **NEEDS WORK** verdict.
