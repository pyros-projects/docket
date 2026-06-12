# Clause Log — mdtodo

Logged at birth during iteration (Phase 4, rule 5). C-NNN ids are per-project
monotonic and survive into `.contracts/mdtodo.contract.yaml` unchanged.

- [C-001] mdtodo MUST resolve its inputs as: each positional path that is a file is scanned as given; each path that is a directory is scanned recursively for `*.md` and `*.markdown` files.
  born: direction lock, in response to "point it at files or a directory, get a list out"
  state-cells: scan-text × success

- [C-002] mdtodo MUST NOT run as a daemon or watch the filesystem — every invocation is a one-shot scan that terminates on its own.
  born: direction lock, rejection: "no daemon, no watching"
  state-cells: (negative — anchored to decision D-002)

- [C-003] Default text output MUST be grouped by file: a header line with the file path (as given on the command line; files discovered under a directory rendered as the given directory path joined with the relative remainder), one line per item of the form `<line>  <marker> <text>` (marker rendered `[ ]`, `TODO:`, or `FIXME:`), blank lines between groups, and a final summary line of the form `<T> TODOs in <M> files (<K> files scanned)`, counts pluralized naturally.
  born: iteration round 1, user accepted v1 layout ("nice")
  state-cells: scan-text × success
  TIGHTENED at round-trip round 1 (leaks 1 + lucky-guess: footer template and directory-path rendering were unpinned).

- [C-004] Output ordering MUST be deterministic: files in lexicographic path order, items within a file in ascending line order, identical in text and JSON modes.
  born: iteration round 1, accepted with v1 layout
  state-cells: scan-text × success

- [C-005] Unchecked GFM task list items (`- [ ]`, `* [ ]`, `+ [ ]`, any leading indentation) MUST be reported as TODOs of kind `task`, with text = the item text after the checkbox.
  born: iteration round 1, in response to "support the usual todo formats"
  state-cells: scan-text × success

- [C-006] Checked task list items (`[x]` or `[X]`) MUST NOT be reported.
  born: iteration round 1, edge probe (formats demo line 4), accepted in round 2 ("good")
  state-cells: scan-text × success

- [C-007] A line containing the marker `TODO:` (uppercase, colon required) MUST be reported as kind `todo`, with text = the remainder of the line after the marker, trimmed, a trailing HTML comment closer `-->` stripped; the marker is recognized anywhere in a line, including inside HTML comments.
  born: iteration round 1, in response to "what counts as a TODO ... support the usual todo formats"
  state-cells: scan-text × success

- [C-008] A line containing the marker `FIXME:` (uppercase, colon required) MUST be reported as kind `fixme`, under the same matching rules as `TODO:`.
  born: iteration round 1, same exchange as C-007
  state-cells: scan-text × success

- [C-009] Lines inside fenced code blocks MUST be scanned under the same rules as any other line — there is no code-block exclusion.
  born: iteration round 1, edge probe (snippet demo), accepted in round 2 ("good")
  state-cells: scan-text × success

- [C-010] With `--json`, mdtodo MUST write a single JSON array to stdout containing one object per TODO item with exactly the fields `file` (path as displayed in text mode), `line` (1-based), `text` (content with the marker stripped), `kind` (`task` | `todo` | `fixme`); zero items yields `[]`.
  born: iteration round 1, in response to "I want to be able to get the output as json too"
  state-cells: scan-json × success, scan-json × empty

- [C-011] Scanning a single 100 MB markdown file MUST keep peak resident memory below 64 MB (line-streaming; no whole-file buffering).
  born: iteration round 1, in response to "it shouldn't choke on big files"; thresholds confirmed at contract time (D-012)
  state-cells: scan-text × success

- [C-012] Scanning a single 100 MB markdown file MUST complete in under 5 seconds wall clock on the reference machine (NVMe-class developer laptop).
  born: iteration round 1, same exchange as C-011; thresholds confirmed at contract time (D-012)
  state-cells: scan-text × success

- [C-013] mdtodo MUST NOT read any configuration file — no `.mdtodorc`, no XDG config, no environment-pointed file; all behavior is controlled by command-line flags only.
  born: iteration round 2, rejection: "drop it, no config file ever, flags only" (kills the v2 `.mdtodorc` sketch)
  state-cells: (negative — anchored to decision D-008)

- [C-014] A file that cannot be read MUST NOT abort the run: mdtodo emits one warning line to stderr, skips the file, continues scanning, and still reports results from readable files.
  born: iteration round 2, in response to "unreadable files shouldn't kill the whole run"
  state-cells: scan-text × permission-denied, scan-text × partial-failure, scan-text × system-failure, scan-json × permission-denied

- [C-015] ~~Exit status MUST follow the mapping: 0 = scan completed with all files readable; 1 = scan completed but ≥1 file unreadable; 2 = invalid invocation.~~
  born: iteration round 2, accepted with the failure-handling demo
  state-cells: scan-text × success, scan-text × partial-failure, usage × validation-failure
  SUPERSEDED at self-admission (A8: three laws in one clause) → split into C-021, C-022, C-023. Not present in the contract file.

- [C-016] When a text-mode scan completes with zero TODOs, mdtodo MUST print exactly one line — `No TODOs found (<N> files scanned).` with the count pluralized naturally — and nothing else to stdout.
  born: iteration round 2, edge probe (empty-result demo), accepted at freeze
  state-cells: scan-text × empty
  AMENDED at round-trip round 2: pluralization wording aligned with C-003 (latent template inconsistency flagged by the blind agent). Interaction with C-024 logged as an open question, not a clause.

- [C-017] In `--json` mode, stdout MUST contain only the JSON document; all warnings and diagnostics go to stderr.
  born: iteration round 2, edge probe (JSON purity under partial failure), accepted at freeze
  state-cells: scan-json × success, scan-json × partial-failure, scan-json × system-failure, scan-json × empty

- [C-018] An invalid invocation (no paths, unknown flag, or a named path that does not exist) MUST be rejected before any scanning begins, with an error line on stderr naming the problem.
  born: iteration round 2, accepted with the usage-error demo
  state-cells: usage × validation-failure

- [C-019] `mdtodo --help` MUST print usage text to stdout and exit 0.
  born: iteration round 2, accepted with the usage-error demo
  state-cells: usage × success

- [C-020] All warning and error lines MUST be single-line, plain-language messages with no stack traces and no internal jargon.
  born: iteration round 2, accepted with the failure-handling demo ("good")
  state-cells: scan-text × permission-denied, usage × validation-failure

- [C-021] A run in which every input file was readable and scanning completed MUST exit 0, regardless of whether any TODOs were found.
  born: self-admission split of C-015 (A8); behavior unchanged from round 2 acceptance; "no TODOs ⇒ still 0" confirmed via options (D-012)
  state-cells: scan-text × success, scan-text × empty, scan-json × success, scan-json × empty

- [C-022] A run in which one or more files were unreadable but scanning otherwise completed MUST exit 1.
  born: self-admission split of C-015 (A8); behavior unchanged from round 2 acceptance
  state-cells: scan-text × partial-failure, scan-json × partial-failure

- [C-023] An invalid invocation MUST exit 2.
  born: self-admission split of C-015 (A8); behavior unchanged from round 2 acceptance
  state-cells: usage × validation-failure

- [C-024] When one or more files were unreadable, the text-mode summary line's parenthetical MUST read `(<R> of <K> files scanned, <U> unreadable)`, where K counts every file selected for scanning and R = K − U.
  born: round-trip round 1, leak 2 — blind reconstruction dropped unreadable files from the scan count; converged transcript (scene 6) reports them
  state-cells: scan-text × partial-failure, scan-text × permission-denied

- [C-025] Every invalid-invocation error line MUST be followed by a one-line usage synopsis (`usage: mdtodo [--json] <path>...`) on stderr.
  born: round-trip round 1, leak 3 — blind reconstruction omitted the synopsis; converged transcript (scene 9) shows it on every usage error
  state-cells: usage × validation-failure
