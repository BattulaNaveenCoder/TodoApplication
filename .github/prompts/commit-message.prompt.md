# Commit Message Prompt

Task:
Generate conventional commit messages for the currently staged changes.

Rules:
- Format: <type>(<scope>): <description>
- Allowed types: feat, fix, test, refactor, docs, chore
- Keep description concise and specific.
- Use present tense and lowercase scope.
- Avoid trailing punctuation.

Output:
1. Primary commit message.
2. Two alternatives.
3. One short body (optional) when change is complex.
