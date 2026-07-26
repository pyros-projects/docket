# External review — Contract Kernel v1 plan

Reviewer: Codie (Codex CLI, gpt-5.6-sol, max reasoning effort), read-only sandbox.
Date: 2026-07-26. Reviewed against clean `main` at 1acd824. No files edited.
Subject: `docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md` plus src/, tests/, and DC-0005.

Commissioned because the in-session multi-persona review returned no content across six agents
and roughly seven hours. This is the only independent read the plan received, and it is
cross-family rather than same-model, which makes it worth more than the six would have been.

---

Not sound as written. The experiment can currently report “go” without demonstrating that any evidence survived change B.

## Would change the plan

1. **[P0] The bench can mistake replacement evidence for carried-forward evidence.**

   Failure scenario — Clauses A and B hold against workspace digest W0. Change B edits a file relevant only to A, producing W1. Because every record compares against the same global digest, both clauses become stale. Running checks again can create W1 records and make B look current, but none of B’s W0 evidence survived.

   Pointer — [plan:210, 333, 383](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:210), [cli.py:129](/home/pyro/projects/agents/docket/src/docket/cli.py:129)

   Confidence — 100%.

   Required change — Use a per-clause subject manifest: declared applicable paths plus acceptance harness and runner configuration. After mutating change B, derive state before running checks or filing anything, and assert that the original evidence file IDs remain admissible for untouched clauses.

2. **[P0] The named bench is not executable or preregistered.**

   Failure scenario — The “existing fixture” references absent tests and scripts, while its prose-only command expectations are deliberately assigned `pending-harness`. During the run, the implementer must invent the subject program, harnesses, changes A/B, and affected-clause set after seeing the mechanism. A friendly case can therefore be manufactured and reported as evidence.

   Pointer — [plan:241, 383](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:241), [fixture:14–25](/home/pyro/projects/agents/docket/fixtures/sfd-variant-run.contract.yaml:14)

   Confidence — 100%.

   Required change — Add a committed synthetic bench before implementing subject validity: tiny working code, exact contract, frozen A and B patches, expected affected clauses, and prohibited evidence operations between mutation and observation.

3. **[P0] The self-governed build is retrospective.**

   Failure scenario — Units 1–7 can add every unnecessary abstraction first. Unit 8 then authors proxies from the implementation and plan file lists already produced. Those proxies pass, and the Definition of Done claims the contract governed the build, although it never constrained most of it.

   Pointer — [plan:246, 361–375, 410](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:246)

   Confidence — 100%.

   Required change — Treat units 1–7 as bootstrap. After unit 8 freezes the contract, perform one separate, real kernel change under the blocking contract. Do not claim the contract governed the code written before it existed.

4. **[P0] The supposedly blocking gate fails open on missing or unproven evidence.**

   Failure scenario — Delete a proxy’s acceptance harness. The runner returns `pending-harness`; no failure is counted, and `docket check --all` exits zero. The existing test explicitly pins that behavior. Adding `unproven` to state and tasks does not alter the gate because unit 7 does not change the CLI failure predicate.

   Pointer — [plan:344–359, 396](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:344), [cli.py:127–162](/home/pyro/projects/agents/docket/src/docket/cli.py:127)

   Confidence — 100%.

   Required change — Make the blocking invocation fail for every active mechanical clause lacking current green proof, including `pending-harness` and `unproven`; add deletion-of-harness as an exit-code test.

5. **[P0] The “many horses” kill condition is not exercised.**

   Failure scenario — The experiment uses a synthetic import fixture and an overengineering contract authored during this same build. No external obligation exists before a subsequent real change and survives without hand-forcing. The verdict can nevertheless mark the condition “not fired” merely because the self-authored contract imported.

   Pointer — [DC-0005:172–180](/home/pyro/projects/agents/docket/memory/decisions/DC-0005-docket-resumes-as-a-contract-kernel-on-one-falsifiable-question.md:172), [plan:361–386](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:361)

   Confidence — 100%.

   Required change — Carry one pre-existing external obligation through the post-bootstrap real change. If that remains outside scope, the terminal verdict must call this kill condition untested and cannot issue an unqualified “go.”

6. **[P1] Subject capture timing can bind a green result to code it never tested.**

   Failure scenario — An acceptance command tests workspace S0, modifies a tracked file, and exits zero. The current control flow runs the subprocess before appending the record. If “at filing time” means computing the digest during append, the evidence records S1 and is considered current even though S1 was never checked.

   Pointer — [plan:327–342](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:327), [cli.py:136–141](/home/pyro/projects/agents/docket/src/docket/cli.py:136)

   Confidence — 75%.

   Required change — Capture the subject before execution, recapture afterward, and admit green evidence only when both digests match. Otherwise record a distinct “workspace mutated during acceptance” failure.

7. **[P1] Removing the signature fiction is acceptable; replacing it with “admission is the only gate” is not.**

   Failure scenario — An agent-generated or PR-supplied contract contains a resolving shell command that exfiltrates credentials or deletes files. The door validates shape and harness availability, imports it, and `check --all` executes it under the developer’s full environment. Repository privacy does not prevent this path.

   Pointer — [plan:252–262](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:252), [runner.py:83–87](/home/pyro/projects/agents/docket/src/docket/runner.py:83)

   Confidence — 100%.

   Judgment — No cryptographic signing is required for this private experiment. The plan does require an explicit trust model: contract YAML is trusted executable code; import is schema admission, not authentication or safety review; only locally reviewed sources may be checked; commands receive the caller’s privileges. The import report should also describe `signed` entries as unverified declarations.

8. **[P1] Verdict validity has two plausible implementations, and both break a stated success condition.**

   Failure scenario — If subject validity applies to verdicts, every workspace change forces Pyro to re-verdict every mechanical clause, contradicting “authority involvement concentrates on residue.” If verdicts remain revision-only, an accepted verdict tied to a stale bundle can combine with a fresh check and produce `holding` without current accepted evidence.

   Pointer — [plan:144, 333, 350](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:144), [state.py:45–63](/home/pyro/projects/agents/docket/src/docket/state.py:45)

   Confidence — 100%.

   Required change — Separate law ratification from evidence verdicts. Mechanical clauses should derive holding from current green proof under ratified law; human-residue clauses derive holding from a current human verdict. A verdict on one bundle must not silently transfer to another subject.

9. **[P1] The run requires amendment and verdict actions that no unit implements or specifies.**

   Failure scenario — Change B requires a clause amendment and the residue requires Pyro’s verdict. The CLI has neither operation, and units 8–9 add neither. The implementer must hand-edit YAML and history JSON or call internal storage methods ad hoc, bypassing the very admission and provenance behavior being evaluated.

   Pointer — [cli.py:10–47](/home/pyro/projects/agents/docket/src/docket/cli.py:10), [plan:377–386](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:377)

   Confidence — 100%.

   Required change — Specify a minimal validated experiment path for amendment and verdict recording. This need not become signing infrastructure or a general product command.

## Worth knowing

1. **The workspace digest is not yet defined as content identity.**

   Hashing HEAD plus staged and unstaged patches can change when identical workspace bytes are merely staged or committed. The exclusion list also misses run reports and other generated outputs; the fixture’s C-019 command itself writes `h.txt`. A sorted manifest of relevant path, mode, and content hashes is cheaper and more robust. Store HEAD separately as provenance.

   Pointer — [plan:210, 317–325, 382](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:210), [fixture:223–228](/home/pyro/projects/agents/docket/fixtures/sfd-variant-run.contract.yaml:223)

   Confidence — 75%.

2. **Clause-content digesting is reasonable, but its canonical payload is undefined.**

   A full model digest makes an edit to `notes` stale evidence; an obligation-only digest misses changed acceptance, scope, or evidence policy. Define the exact normative fields and canonical serialization. The cheaper integrity mechanism is to store each clause’s resulting digest in its amendment record and report an unrecorded edit as tampered law; evidence can retain the existing per-clause revision floor.

   Pointer — [plan:211, 333–340](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:211)

   Confidence — 75%.

3. **The generic intent abstraction does not yet earn its full shape.**

   A door check that counts any non-human acceptance can accept a prose-only command as a “mechanical proxy,” even though unit 3 deliberately makes that command pending. The explicit no-residue escape also weakens the settled qualitative shape.

   For this experiment, require a structured, executable proxy and an actual human residue. A minimal shared intent identifier is earned; a general intent registry plus no-residue branch should wait for a second consumer.

   Pointer — [plan:209, 212, 361–375](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:209)

   Confidence — 75%.

4. **The anchor design still has three sources, not one.**

   Runtime and two producer documents remain independently edited lists; a drift test detects some divergence but does not make them share one source. Either introduce a small canonical manifest used to generate/check producer text or weaken the requirement from “exactly one source” to “three synchronized representations.”

   Pointer — [plan:81, 208, 264–277](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:81)

   Confidence — 100%.

5. **The eleven fault injections cannot literally produce eleven distinct states.**

   Several acceptance examples intentionally converge on `stale` or `broken`; import refusal and producer admissibility are transaction outcomes, not clause states. A matrix of expected observable, exit code, state, and message would avoid implementers inventing artificial state names to satisfy the wording.

   Pointer — [plan:128–140, 377–398](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:128)

   Confidence — 100%.

## Confirmed, no finding

- **KTD4’s factual claim is correct.** `last_amend_rev` filters amendment changes by clause ID, and state derives a separate floor for each clause before filtering bundles, checks, and verdicts. Editing contract YAML without an amendment leaves that floor unchanged, so current evidence remains valid. [storage.py:96–99](/home/pyro/projects/agents/docket/src/docket/storage.py:96), [state.py:43–49](/home/pyro/projects/agents/docket/src/docket/state.py:43)

- **The `unproven` precedence insertion is correct.** Putting it after structural flags and before `holding` preserves stronger states and does not shadow `broken`, `stale`, `pending-harness`, or `overlap`.

- **The pinned-test reversals are handled coherently.** Unit 4 explicitly recognizes both partial-import cases, including the cross-contract collision test, while unit 7 corrects and renames the empty-evidence “all green” test. No deletion is proposed.

Reviewed against clean `main` at `1acd824`; no files were edited. Historical memory was used only for boundary orientation and was rechecked against the live repository.


tokens used
241,270
Not sound as written. The experiment can currently report “go” without demonstrating that any evidence survived change B.

## Would change the plan

1. **[P0] The bench can mistake replacement evidence for carried-forward evidence.**

   Failure scenario — Clauses A and B hold against workspace digest W0. Change B edits a file relevant only to A, producing W1. Because every record compares against the same global digest, both clauses become stale. Running checks again can create W1 records and make B look current, but none of B’s W0 evidence survived.

   Pointer — [plan:210, 333, 383](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:210), [cli.py:129](/home/pyro/projects/agents/docket/src/docket/cli.py:129)

   Confidence — 100%.

   Required change — Use a per-clause subject manifest: declared applicable paths plus acceptance harness and runner configuration. After mutating change B, derive state before running checks or filing anything, and assert that the original evidence file IDs remain admissible for untouched clauses.

2. **[P0] The named bench is not executable or preregistered.**

   Failure scenario — The “existing fixture” references absent tests and scripts, while its prose-only command expectations are deliberately assigned `pending-harness`. During the run, the implementer must invent the subject program, harnesses, changes A/B, and affected-clause set after seeing the mechanism. A friendly case can therefore be manufactured and reported as evidence.

   Pointer — [plan:241, 383](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:241), [fixture:14–25](/home/pyro/projects/agents/docket/fixtures/sfd-variant-run.contract.yaml:14)

   Confidence — 100%.

   Required change — Add a committed synthetic bench before implementing subject validity: tiny working code, exact contract, frozen A and B patches, expected affected clauses, and prohibited evidence operations between mutation and observation.

3. **[P0] The self-governed build is retrospective.**

   Failure scenario — Units 1–7 can add every unnecessary abstraction first. Unit 8 then authors proxies from the implementation and plan file lists already produced. Those proxies pass, and the Definition of Done claims the contract governed the build, although it never constrained most of it.

   Pointer — [plan:246, 361–375, 410](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:246)

   Confidence — 100%.

   Required change — Treat units 1–7 as bootstrap. After unit 8 freezes the contract, perform one separate, real kernel change under the blocking contract. Do not claim the contract governed the code written before it existed.

4. **[P0] The supposedly blocking gate fails open on missing or unproven evidence.**

   Failure scenario — Delete a proxy’s acceptance harness. The runner returns `pending-harness`; no failure is counted, and `docket check --all` exits zero. The existing test explicitly pins that behavior. Adding `unproven` to state and tasks does not alter the gate because unit 7 does not change the CLI failure predicate.

   Pointer — [plan:344–359, 396](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:344), [cli.py:127–162](/home/pyro/projects/agents/docket/src/docket/cli.py:127)

   Confidence — 100%.

   Required change — Make the blocking invocation fail for every active mechanical clause lacking current green proof, including `pending-harness` and `unproven`; add deletion-of-harness as an exit-code test.

5. **[P0] The “many horses” kill condition is not exercised.**

   Failure scenario — The experiment uses a synthetic import fixture and an overengineering contract authored during this same build. No external obligation exists before a subsequent real change and survives without hand-forcing. The verdict can nevertheless mark the condition “not fired” merely because the self-authored contract imported.

   Pointer — [DC-0005:172–180](/home/pyro/projects/agents/docket/memory/decisions/DC-0005-docket-resumes-as-a-contract-kernel-on-one-falsifiable-question.md:172), [plan:361–386](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:361)

   Confidence — 100%.

   Required change — Carry one pre-existing external obligation through the post-bootstrap real change. If that remains outside scope, the terminal verdict must call this kill condition untested and cannot issue an unqualified “go.”

6. **[P1] Subject capture timing can bind a green result to code it never tested.**

   Failure scenario — An acceptance command tests workspace S0, modifies a tracked file, and exits zero. The current control flow runs the subprocess before appending the record. If “at filing time” means computing the digest during append, the evidence records S1 and is considered current even though S1 was never checked.

   Pointer — [plan:327–342](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:327), [cli.py:136–141](/home/pyro/projects/agents/docket/src/docket/cli.py:136)

   Confidence — 75%.

   Required change — Capture the subject before execution, recapture afterward, and admit green evidence only when both digests match. Otherwise record a distinct “workspace mutated during acceptance” failure.

7. **[P1] Removing the signature fiction is acceptable; replacing it with “admission is the only gate” is not.**

   Failure scenario — An agent-generated or PR-supplied contract contains a resolving shell command that exfiltrates credentials or deletes files. The door validates shape and harness availability, imports it, and `check --all` executes it under the developer’s full environment. Repository privacy does not prevent this path.

   Pointer — [plan:252–262](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:252), [runner.py:83–87](/home/pyro/projects/agents/docket/src/docket/runner.py:83)

   Confidence — 100%.

   Judgment — No cryptographic signing is required for this private experiment. The plan does require an explicit trust model: contract YAML is trusted executable code; import is schema admission, not authentication or safety review; only locally reviewed sources may be checked; commands receive the caller’s privileges. The import report should also describe `signed` entries as unverified declarations.

8. **[P1] Verdict validity has two plausible implementations, and both break a stated success condition.**

   Failure scenario — If subject validity applies to verdicts, every workspace change forces Pyro to re-verdict every mechanical clause, contradicting “authority involvement concentrates on residue.” If verdicts remain revision-only, an accepted verdict tied to a stale bundle can combine with a fresh check and produce `holding` without current accepted evidence.

   Pointer — [plan:144, 333, 350](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:144), [state.py:45–63](/home/pyro/projects/agents/docket/src/docket/state.py:45)

   Confidence — 100%.

   Required change — Separate law ratification from evidence verdicts. Mechanical clauses should derive holding from current green proof under ratified law; human-residue clauses derive holding from a current human verdict. A verdict on one bundle must not silently transfer to another subject.

9. **[P1] The run requires amendment and verdict actions that no unit implements or specifies.**

   Failure scenario — Change B requires a clause amendment and the residue requires Pyro’s verdict. The CLI has neither operation, and units 8–9 add neither. The implementer must hand-edit YAML and history JSON or call internal storage methods ad hoc, bypassing the very admission and provenance behavior being evaluated.

   Pointer — [cli.py:10–47](/home/pyro/projects/agents/docket/src/docket/cli.py:10), [plan:377–386](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:377)

   Confidence — 100%.

   Required change — Specify a minimal validated experiment path for amendment and verdict recording. This need not become signing infrastructure or a general product command.

## Worth knowing

1. **The workspace digest is not yet defined as content identity.**

   Hashing HEAD plus staged and unstaged patches can change when identical workspace bytes are merely staged or committed. The exclusion list also misses run reports and other generated outputs; the fixture’s C-019 command itself writes `h.txt`. A sorted manifest of relevant path, mode, and content hashes is cheaper and more robust. Store HEAD separately as provenance.

   Pointer — [plan:210, 317–325, 382](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:210), [fixture:223–228](/home/pyro/projects/agents/docket/fixtures/sfd-variant-run.contract.yaml:223)

   Confidence — 75%.

2. **Clause-content digesting is reasonable, but its canonical payload is undefined.**

   A full model digest makes an edit to `notes` stale evidence; an obligation-only digest misses changed acceptance, scope, or evidence policy. Define the exact normative fields and canonical serialization. The cheaper integrity mechanism is to store each clause’s resulting digest in its amendment record and report an unrecorded edit as tampered law; evidence can retain the existing per-clause revision floor.

   Pointer — [plan:211, 333–340](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:211)

   Confidence — 75%.

3. **The generic intent abstraction does not yet earn its full shape.**

   A door check that counts any non-human acceptance can accept a prose-only command as a “mechanical proxy,” even though unit 3 deliberately makes that command pending. The explicit no-residue escape also weakens the settled qualitative shape.

   For this experiment, require a structured, executable proxy and an actual human residue. A minimal shared intent identifier is earned; a general intent registry plus no-residue branch should wait for a second consumer.

   Pointer — [plan:209, 212, 361–375](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:209)

   Confidence — 75%.

4. **The anchor design still has three sources, not one.**

   Runtime and two producer documents remain independently edited lists; a drift test detects some divergence but does not make them share one source. Either introduce a small canonical manifest used to generate/check producer text or weaken the requirement from “exactly one source” to “three synchronized representations.”

   Pointer — [plan:81, 208, 264–277](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:81)

   Confidence — 100%.

5. **The eleven fault injections cannot literally produce eleven distinct states.**

   Several acceptance examples intentionally converge on `stale` or `broken`; import refusal and producer admissibility are transaction outcomes, not clause states. A matrix of expected observable, exit code, state, and message would avoid implementers inventing artificial state names to satisfy the wording.

   Pointer — [plan:128–140, 377–398](/home/pyro/projects/agents/docket/docs/plans/2026-07-26-001-feat-contract-kernel-v1-plan.md:128)

   Confidence — 100%.

## Confirmed, no finding

- **KTD4’s factual claim is correct.** `last_amend_rev` filters amendment changes by clause ID, and state derives a separate floor for each clause before filtering bundles, checks, and verdicts. Editing contract YAML without an amendment leaves that floor unchanged, so current evidence remains valid. [storage.py:96–99](/home/pyro/projects/agents/docket/src/docket/storage.py:96), [state.py:43–49](/home/pyro/projects/agents/docket/src/docket/state.py:43)

- **The `unproven` precedence insertion is correct.** Putting it after structural flags and before `holding` preserves stronger states and does not shadow `broken`, `stale`, `pending-harness`, or `overlap`.

- **The pinned-test reversals are handled coherently.** Unit 4 explicitly recognizes both partial-import cases, including the cross-contract collision test, while unit 7 corrects and renames the empty-evidence “all green” test. No deletion is proposed.

Reviewed against clean `main` at `1acd824`; no files were edited. Historical memory was used only for boundary orientation and was rechecked against the live repository.


