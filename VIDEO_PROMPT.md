# Investor-style video prompt

Use the following prompt with a video creation tool. Supply your own genuine dashboard and Switch room screen recordings as source footage. Replace bracketed material only with verified facts; do not fabricate customer traction, agent activity, integration, or test results.

> Create a 75–90 second investor-style product pitch for **IncidentRoom AI**, a human-led incident response workspace built for the Flip the Switch Hackathon. Style: polished, modern B2B software launch, dark navy backgrounds, restrained lime accents, crisp typography, subtle motion, calm confident narration, and a clear story arc. Use the supplied real product footage; do not invent a working Switch integration or customer metrics.
>
> **Opening (0–12s):** Show an engineer facing scattered alerts and a checkout error. Narration: “When checkout goes down, every minute is spent piecing together what happened, who owns the fix, and whether it is safe to ship.”
>
> **Product (12–35s):** Transition to the real IncidentRoom dashboard. Highlight incident state, response playbook, and activity. Narration: “IncidentRoom brings the response into focus: triage, investigation, a proposed repair, human review, and verification in one visible workflow.” Add on-screen labels: “Signal → Evidence → Approval → Verification.”
>
> **How it works (35–60s):** Show the terminal command `python dashboard_server.py`, then open `http://127.0.0.1:8080`. Show the person clicking Start triage, reviewing the proposed change and hash, and clicking Approve fix & run tests. Briefly show the optional commands `python incident.py triage`, `python incident.py status`, and `python incident.py approve <full-sha256>` as alternatives in a separate freshly reset fixture; do not execute both paths on the same completed run. Show the verified status and passing tests only if the recorded run actually passes. Narration: “For this checkout example, the local workflow proposes a targeted fix. A person reviews the exact change and approves it before the regression tests run.”
>
> **Collaboration (60–75s):** If real Switch footage is available, show the actual Mattermost conversation and agent handoffs. Otherwise show the room setup instructions and label this section “Switch integration: setup required.” Narration: “With Switch, the intended workflow brings people and coding agents together in a shared team room.”
>
> **Close (75–90s):** Return to the real dashboard. Narration: “IncidentRoom AI: clearer decisions, accountable action, and a more confident path from incident to resolution.” End card: “IncidentRoom AI · Human-led incident response” and [actual repository URL].
>
> Avoid fictional testimonials, fabricated production deployments, fake metrics, or claims that the sample has been tested with Switch unless there is real footage proving it. The dashboard is a local demo, the approval gate is local, and the sample is not a production incident platform.
