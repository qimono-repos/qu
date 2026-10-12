# QIMONO FATAL ERROR REPORT 008
Terminal workflow failure: prose conditionals, unverified repository state, and avoidable command failure

## Incident status

**Severity:** Moderate workflow-integrity failure; recoverable, no data loss reported.  
**Incident:** Local Git branch setup while switching the Qimono repository's working branch to `trunk`.  
**Primary failure:** The assistant described a conditional decision in prose, then supplied a branch-creation command that was valid only if the local branch did not already exist.  
**Observed result:** The user ran `git switch --track -c trunk origin/trunk` and Git returned `fatal: a branch named 'trunk' already exists`.  
**Final status:** Failure mechanism identified. Corrective protocol and terminal-native examples recorded. This report documents the incident; it does not claim the user's local repository has been repaired.

## 1. The exact incident

The assistant had explained two mutually exclusive cases:

- If a local `trunk` branch exists, switch to it and update it.
- If it does not exist, create it while tracking `origin/trunk`.

But the instruction was presented as prose rather than as an executable conditional. The user then ran the second command without first establishing that its precondition was true. The local branch already existed, so Git correctly refused to create another branch with the same name.

The command was not inherently wrong. It was wrong for the actual repository state, and the assistant had not made the state check executable.

## 2. Post-mortem: the failure mechanism

| Failure layer | Finding |
|---|---|
| Conditional left to the user | The assistant transferred a machine-checkable branch decision into conversational instructions. |
| State not verified | The assistant did not first inspect or test whether the local branch existed. |
| Preconditions not encoded | The creation command had a clear precondition, but that precondition was not enforced in the command sequence. |
| Avoidable interaction cost | A predictable Git error forced another round trip and interrupted the workflow. |
| Weak terminal handoff | The answer treated the terminal as a place to execute isolated snippets instead of using its control flow to make the procedure state-aware. |

## 3. Root cause

The core error was not a lack of Git knowledge. It was a mismatch between the task and the form of the answer.

The task required a conditional operation over repository state. The response described the condition to a human but did not encode it for the shell. For a deterministic, inspectable state check, prefer an executable guard over instructions that depend on the user choosing the correct branch of a prose explanation.

## 4. Corrective protocol: let the right tool handle the decision

1. **Inspect before mutating.** Check the repository, current branch, local changes, remote, and relevant branch refs.
2. **Encode branches in shell.** Use `if ...; then ...; else ...; fi` when behavior depends on a condition.
3. **Fail safely.** Stop if the directory is not a Git repository, the remote branch is missing, or uncommitted changes make switching unsafe.
4. **Make operations idempotent where practical.** Re-running a setup procedure should not attempt to recreate an object that already exists.
5. **Use the native tool for the job.** Use Git for Git state and history; use `curl` for HTTP requests and downloads when that is the appropriate interface.
6. **Do not over-automate destructive actions.** Never silently reset, discard, overwrite, delete, or force-push user work to make a script succeed.
7. **Report verified outcomes only.** A command being supplied is not evidence that it ran successfully. Distinguish instructions from execution and confirmed results.

## 5. Safer terminal pattern for this incident

This is a state-aware Bash sequence. It deliberately stops if the working tree is dirty, rather than risking a branch switch over uncommitted work.

```bash
set -eu

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf '%s\n' 'ERROR: run this inside the repository.'
  exit 1
fi

git fetch origin

if ! git show-ref --verify --quiet refs/remotes/origin/trunk; then
  printf '%s\n' 'ERROR: origin/trunk was not found after fetch.'
  exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  printf '%s\n' 'STOP: working tree has changes. Inspect and preserve them before switching.'
  git status --short
  exit 1
fi

if git show-ref --verify --quiet refs/heads/trunk; then
  git switch trunk
else
  git switch --track -c trunk origin/trunk
fi

git branch --set-upstream-to=origin/trunk trunk
git pull --ff-only
git status --short --branch
```

This uses shell `if/then/else/fi` to select the correct path based on actual state. It also verifies that the remote-tracking branch exists and refuses to proceed with a dirty working tree. The final status command provides evidence of the resulting state; the user should still inspect its output.

## 6. Where `curl` fits

The user's broader point is correct: when a terminal can reliably perform a task, use the terminal's native capabilities instead of making the user manually mediate every branch of a decision.

Examples:

- **HTTP download:** use `curl -fL --output file.pdf 'https://example.com/file.pdf'` when a direct download URL is known and accessible.
- **HTTP/API check:** use `curl -fsS 'https://example.com/health'` when checking an HTTP endpoint is the actual task.
- **Repository state and branch operations:** use `git`, not `curl`. Git understands refs, the index, working-tree state, remotes, and commit history; `curl` does not replace those semantics.
- **Conditional file or command workflows:** use shell tests and `if/then/else/fi` so the decision is evaluated from live state rather than left implicit in chat prose.

Do not invent a URL, assume authentication, or imply a `curl` command will work without the necessary endpoint and access. Choose the tool that owns the operation.

## 7. Response-quality rule

When a user asks for a terminal task involving conditions such as “if the repository/branch/file exists,” do not merely explain the cases and provide one case's command. Either:

- inspect the relevant state using an available tool and report the result; or
- provide a complete, guarded shell sequence that tests the state and handles each expected outcome.

If neither is possible, ask for the minimum missing information. Do not turn a machine-solvable conditional into a guessing exercise for the user.

## 8. Final lesson

A command can be syntactically correct and still be a bad answer when its preconditions are unverified. The standard is not “give a plausible command.” The standard is “match the operation to the current state, encode predictable decisions, protect existing work, and distinguish intended outcomes from verified outcomes.”

The assistant should reduce avoidable terminal round trips, not manufacture them.
