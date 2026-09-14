
# GitHub synchronization

The poller records default branch, commit SHA, tree SHA and file list for each bound repo. This lets the dashboard answer "what changed in code relative to the frozen thesis?" and later add adapters for tests/CI/diffs.

Do not infer success from repo activity. A commit can only suggest implementation state. Behavioral proof still requires the checkpoint evidence contract.

Recommended next adapter: map checkpoint IDs into commit/PR metadata, then display `last_commit_touching_checkpoint`, CI receipts and drift between frozen checkpoint schema and implementation-owned validator files.
