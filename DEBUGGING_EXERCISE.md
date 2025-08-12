# LangChain Debugging Exercise - Exam

## Objective
Demonstrate your debugging skills by identifying and fixing bugs in a LangChain application using the help of LLM.

## Setup
1. Ensure you have your Google API key set in `.env`
2. Install dependencies: `uv sync` or `pip install -r requirements.txt`

## Your Task
This LangChain application contains **5 intentional bugs**. Your job is to:

1. **Find each bug** by running and testing the application
2. **Use an LLM** to help with debugging
3. **Fix each bug** and verify the solution works
4. **Document your debugging process**

## Getting Started
Run the application to begin identifying issues:
```bash
uv run demo.py
# or
uv run main.py
```

Test different functionalities to discover all bugs.

## Documentation Required

For each bug you find and fix, write in a file call `DEBUGGING_FINDINGS.md` that has the following details:

```markdown
## Bug #X: [Brief Description]

**Error/Issue Observed:**
[Describe what went wrong]

**LLM Assistance Used:**
[Summarize how you used the LLM to help debug]

**Root Cause:**
[What was actually wrong]

**Fix Applied:**
[Show the code changes you made]


**Verification:**
[How you confirmed the fix worked]
```

## Success Criteria

Your submission is complete when:
- [ ] All bugs are identified and fixed
- [ ] The application runs without errors
- [ ] All features work as expected
- [ ] Documentation (DEBUGGING_FINDINGS.md) is provided for each bug
- [ ] You can demonstrate the working application

## Submission
Submit your solution to Github. Attach the github link to the exam form.

## Notes
- You may use any LLM tool to assist with debugging
- Focus on understanding the root cause, not just applying fixes
- Test thoroughly to ensure your fixes don't introduce new issues