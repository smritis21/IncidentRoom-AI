# IncidentRoom AI

A small, human-led incident desk for a broken checkout. A team can use four coding agents in a Switch room to triage, investigate, propose a repair and verify it. A reproducible local fixture and approval gate make the demonstration concrete.

**Status:** The local workflow is deterministic, uses no model, and is independently runnable. The Switch room setup below is a documented integration using Switch Console's managed coding agents; it has **not been connected or tested in a live Switch installation here**. The role scripts do not themselves speak the Switch protocol. Do not present their local transcript as a real agent conversation. A real Switch room, provider credentials and a recorded chat demo are still required for the hackathon.

## The incident

`checkout.py` deliberately calls `upper()` on an optional coupon. Requests without a coupon return HTTP 500. `logs/incident.log` is synthetic sample evidence. The proposed one-line fix handles a missing coupon; the verifier runs regression tests. The sample is local only and never deploys anything.

## Quick start (Python 3.9+, no dependencies)

From this folder, in PowerShell or a terminal:

```sh
python incident.py triage
python incident.py status
```

Review the printed one-line change and the proposed SHA-256. To approve and apply exactly that proposed file, copy the full hash from the output:

```sh
python incident.py approve <full-sha256>
python incident.py status
```

The gate checks the original source and proposed file hashes before writing; a stale source or incorrect hash fails closed. It then runs the regression suite and reports verification failure if tests fail. Approval is a **local command by whoever has filesystem access**, not authenticated Switch identity or a production security boundary. There is no deployment or automatic rollback. State is in ignored `.incident-state.json`; it is a local audit aid, not tamper-proof. The sample fix is deliberately specific to this fixture; this is not a general incident diagnosis system. Do not run it on production code.

To see the actual HTTP failure before approval, start `python checkout.py` in a second terminal and send a POST to `http://127.0.0.1:8081/checkout` with JSON `{"cents":1000}`. Repeat after repair; the result becomes `{"total_cents": 1000}`. Stop the server and restart it after editing, because Python loaded the old code into memory.

Run `python -m unittest discover -s tests -v` after approval. Before repair the missing-coupon test is expected to fail. To reset the fixture, restore `checkout.py` from the original archive or run `git restore checkout.py` in a clean checkout; delete `.incident-state.json` if desired. This overwrites the sample file, so preserve any changes first.

## Connect to Switch

1. Install [Switch Console](https://github.com/sandbox-quantum/switch), start its local server and Mattermost following the [official quickstart](https://github.com/sandbox-quantum/switch#readme). Configure an available coding provider such as Codex or Claude Code and its credentials. Windows/Linux support may vary by release.
2. In Console, create a room named `incident-room`, linked to Mattermost, add yourself, and create four managed coding agents: `triage`, `investigator`, `fixer`, and `verifier`. Set each agent's working directory to this project folder and paste the corresponding role in [switch/ROOM.md](switch/ROOM.md) into its instructions. Give the agents only the permissions needed for this disposable fixture; set addressing and access policies appropriate to your team.
3. In the actual Mattermost room, post the kickoff from [switch/ROOM.md](switch/ROOM.md). Agents should use room mentions to hand work onward and post their evidence there. Ask the fixer to run `python incident.py triage` and share the exact hash and proposed change. Review the change yourself and execute `python incident.py approve <hash>` locally; then ask the verifier to inspect status and run tests. Do not assume an agent's chat message is an authenticated approval to the local gate.
4. Record the real room conversation, approval, and test result. Console UI and agent behavior depend on the installed version/provider; verify the room and permissions before recording. The handoffs are agent instructions, not enforced orchestration, and agents may need prompting. The local workflow does not publish events to Switch automatically.

Switch provides the room, chat bridge and agent runtime. This project supplies the incident fixture, guard, tests and room roles. See [Switch repository](https://github.com/sandbox-quantum/switch) and the [hackathon overview](https://www.wemakedevs.org/hackathons/switch) for current setup and rules.

## Files

- `checkout.py`, `logs/incident.log`: intentionally broken sample and synthetic incident evidence.
- `incident.py`: deterministic triage, exact-file approval and verification, with local JSON event record.
- `tests/`: regression and approval gate tests.
- `switch/ROOM.md`: real-room setup and agent instructions.
- `DEMO.md`, `SUBMISSION.md`: recording plan and submission draft.

## Limitations

The sample proposal recognizes one known bug; it does not infer arbitrary fixes. Switch setup, actual AI collaboration, chat identity, and a video have not been verified or generated. No public repository has been created. Avoid real incident data, secrets and production credentials in a public demo.
