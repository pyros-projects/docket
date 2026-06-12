# mdtodo — converged surface prototype (scripted session transcript)

Surface type: CLI. This transcript IS the prototype: every scene below was
demonstrated to and accepted by the user. v3 = converged 2026-06-12 (v1: base
scanner; v2: formats + --json + big files + .mdtodorc sketch; v3: .mdtodorc
removed, failure handling and exit codes added).

Demo fixture tree used throughout:

```
demo/
  docs/
    api.md          (clean — no TODOs)
    roadmap.md      (task item at line 12, TODO: at line 40)
    setup.md        (FIXME: at line 8)
  clean/            (2 clean files)
  formats.md        (format demo)
  snippet.md        (fenced code block demo)
  notes.md          (task item at line 3, TODO: at line 17)
  private.md        (mode 000 — unreadable)
  huge-export.md    (100 MB generated file)
```

---

## Scene 1 — happy path, text output (default)

```
$ mdtodo demo/docs demo/notes.md

demo/docs/roadmap.md
  12  [ ] ship the v0.2 changelog
  40  TODO: decide on the plugin API surface

demo/docs/setup.md
   8  FIXME: brew formula is outdated

demo/notes.md
   3  [ ] call the venue about parking
  17  TODO: archive last year's notes

5 TODOs in 3 files (4 files scanned)

$ echo $?
0
```

Notes: grouped by file; files in lexicographic path order; items in ascending
line order; files without TODOs (demo/docs/api.md) are scanned but produce no
group; summary footer always last.

## Scene 2 — what counts as a TODO (format demo, round-1 edge probes)

```
$ cat demo/formats.md
# Format demo

- [ ] an open task item
- [x] a completed task item
* [ ] open item with star bullet
Remember TODO: rotate the API keys
FIXME: the diagram below is stale
<!-- TODO: hook up CI for this page -->
todo: lowercase is prose, not a marker

$ mdtodo demo/formats.md

demo/formats.md
   3  [ ] an open task item
   5  [ ] open item with star bullet
   6  TODO: rotate the API keys
   7  FIXME: the diagram below is stale
   8  TODO: hook up CI for this page

5 TODOs in 1 file (1 file scanned)
```

Accepted rules demonstrated here:
- Unchecked GFM task items (`- [ ]`, `* [ ]`, `+ [ ]`, any indentation) count; the
  bullet is dropped in display, the checkbox is rendered `[ ]`.
- Checked items (`[x]`/`[X]`, line 4) are NOT reported.
- `TODO:` / `FIXME:` markers — uppercase with colon — count anywhere in a line,
  including inside HTML comments (line 8; trailing `-->` stripped from the text).
- Lowercase `todo:` (line 9) is prose, not a marker.

## Scene 3 — fenced code blocks are scanned (round-1 edge probe)

```
$ cat demo/snippet.md
# Snippet

```python
# TODO: refactor this helper
def f():
    ...
```

$ mdtodo demo/snippet.md

demo/snippet.md
   4  TODO: refactor this helper

1 TODO in 1 file (1 file scanned)
```

No code-block exclusion: a TODO in a code sample is still a TODO.

## Scene 4 — JSON output

```
$ mdtodo --json demo/docs demo/notes.md
[
  {"file": "demo/docs/roadmap.md", "line": 12, "text": "ship the v0.2 changelog", "kind": "task"},
  {"file": "demo/docs/roadmap.md", "line": 40, "text": "decide on the plugin API surface", "kind": "todo"},
  {"file": "demo/docs/setup.md", "line": 8, "text": "brew formula is outdated", "kind": "fixme"},
  {"file": "demo/notes.md", "line": 3, "text": "call the venue about parking", "kind": "task"},
  {"file": "demo/notes.md", "line": 17, "text": "archive last year's notes", "kind": "todo"}
]
$ echo $?
0
```

Notes: one object per item; fields exactly `file`, `line` (1-based), `text`
(content with the marker stripped), `kind` (`task` | `todo` | `fixme`); same
ordering as text mode.

## Scene 5 — big file (round-1: "shouldn't choke on big files")

```
$ ls -lh demo/huge-export.md
-rw-r--r--  1 user  user  100M Jun 12 09:14 demo/huge-export.md

$ /usr/bin/time -v mdtodo demo/huge-export.md

demo/huge-export.md
  1048576  TODO: re-check this import batch

1 TODO in 1 file (1 file scanned)

	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:03.10
	Maximum resident set size (kbytes): 38912
```

Streams line by line — memory stays flat regardless of file size.

## Scene 6 — unreadable file: warn, skip, continue (round 2)

```
$ ls -l demo/private.md
----------  1 root  root  2048 Jun 12 09:14 demo/private.md

$ mdtodo demo/docs demo/private.md
warning: cannot read demo/private.md: permission denied

demo/docs/roadmap.md
  12  [ ] ship the v0.2 changelog
  40  TODO: decide on the plugin API surface

demo/docs/setup.md
   8  FIXME: brew formula is outdated

3 TODOs in 2 files (3 of 4 files scanned, 1 unreadable)

$ echo $?
1
```

Warning goes to stderr; readable results still print; exit 1 signals partial.

## Scene 7 — JSON mode stays pure under partial failure (round-2 edge probe)

```
$ mdtodo --json demo/docs demo/private.md 2>warnings.txt
[
  {"file": "demo/docs/roadmap.md", "line": 12, "text": "ship the v0.2 changelog", "kind": "task"},
  {"file": "demo/docs/roadmap.md", "line": 40, "text": "decide on the plugin API surface", "kind": "todo"},
  {"file": "demo/docs/setup.md", "line": 8, "text": "brew formula is outdated", "kind": "fixme"}
]
$ cat warnings.txt
warning: cannot read demo/private.md: permission denied
$ echo $?
1
```

stdout is only the JSON document — always parseable, even with warnings.

## Scene 8 — empty result (round-2 edge probe)

```
$ mdtodo demo/clean
No TODOs found (2 files scanned).
$ echo $?
0

$ mdtodo --json demo/clean
[]
$ echo $?
0
```

Finding nothing is success, not an error.

## Scene 9 — usage errors and help (round 2)

```
$ mdtodo
error: no paths given
usage: mdtodo [--json] <path>...
$ echo $?
2

$ mdtodo --watch demo
error: unknown flag: --watch
usage: mdtodo [--json] <path>...
$ echo $?
2

$ mdtodo missing/
error: path does not exist: missing/
$ echo $?
2

$ mdtodo --help
usage: mdtodo [--json] <path>...

Scan markdown files and list TODO items.

  <path>...   files or directories (directories are searched recursively
              for *.md and *.markdown)
  --json      emit a JSON array instead of text output
  --help      show this help

exit codes: 0 ok · 1 some files unreadable · 2 usage error
$ echo $?
0
```

Errors go to stderr, name the problem, and nothing is scanned. No config file
exists or is ever looked for — the rejected `.mdtodorc` sketch from v2 is gone.
