# School controllers and HQ oversight

The live simulation is self-contained and rule-driven. An optional Gemini adapter now supplies manually requested advice through a visitor-owned connection. No external service is required to use the simulation.

The physical simulation, policy decision layer and interface are separate concerns. Timetables, movement, battery and resource availability are facts owned by the deterministic simulation engine. AI can interpret those observations and recommend action; it should not invent a new state to make a task appear successful.

## Present runtime

```text
JSON school / robot / zone / schedule inputs
                    |
          HQSimulation shared clock
                    |
     24 SchoolAgent controller instances
  (own jobs, robots, operators, lift, timetable)
                    |
    school observations + local action records
                    |
      HQ aggregation / outside-policy queue
                    |
    observe        decide         assess
       human follow-up -> relevant school queue
```

The 24 instances are independent domain contexts in one browser process. They are not 24 language-model conversations today. The simulation clock can advance rapidly without making any model requests. Controller rules are visible in the activity feed.

## Optional Gemini advice now implemented

`js/gemini.js` calls Google's generateContent endpoint directly with the visitor's own in-memory key. `js/connection.js` provides Connect & test, Disconnect and per-exception Ask Gemini. A real test generation must succeed before connected status appears. There is no saved/shared key or server. Future shared organisation credentials must be held on a server.

Each request contains one school exception's facts and current editable settings. No other school's robot telemetry is included. The model returns a recommendation enum, brief summary and fact-key evidence. The client validates that shape and evidence keys; prose remains model advice and can be wrong. It is displayed as text, never executed. Human approval buttons continue to call the original simulation controller. The 24 school controllers are still deterministic, not autonomous model conversations.

A request pauses the clock. Changed simulation identity, minute, rule revision or incident status causes a pending reply to be discarded. Accepted advice becomes labelled historical if the minute or rule revision changes. It is held outside simulation snapshots, and disconnect clears it. No secrets or AI advice are added to exported runs.

The adapter allows only the reviewed model ID, caps generation attempts at 10 per visit, spaces attempts by 15 seconds, and disconnects on access or quota rejection. No model fallback, automatic retries or paid upgrades occur. Limits are per page, not account-wide. A user confirms Free Tier and billing-off; the adapter cannot independently verify their project's billing state. Only fictional data is appropriate for this prototype.

The `agents/` definitions and `schema/agent-proposal.schema.json` remain future autonomous-agent interface scaffolding; they are not the contract used by this smaller manual-advice adapter. Production agent autonomy, shared server credentials, durable audit trails and multi-user orchestration remain future work.

## HQ versus cleaning supervisor

Both audiences should read the same underlying school state and job IDs.

- HQ sees cross-school utilisation, recurring service failures, intervention burden, missed work and significant follow-up. It sets or reviews operating policy and coordinates contractor/vendor support.
- The cleaning supervisor sees the school's robot locations, upcoming tasks, preparation, local recovery instructions, remaining manual work and completion/reporting records.

A future authenticated server must enforce view and command permissions; hiding other schools in a dropdown is not access control. The browser-only prototype does not claim production authentication or multi-user consistency.

## Persistent execution later

Browser execution stops when the page is closed and may be throttled in the background. GitHub Pages serves the application files; it cannot host an always-running simulation or hide model credentials.

For persistent two-year runs and shared viewing, move the same clock, school controllers, action queue and state snapshots to a backend. Stream observations to HQ and school interfaces. Store append-only events and periodic snapshots for audit and reporting; do not rely on a browser's short feed as the historical record.

## Editable operating policy

Principles are maintained in `config/principles.json`, structured condition/action rules in `config/rules.json`, and schedule/model settings in `config/simulation.json`. The browser editor validates and applies these without executing user-supplied scripts. This is the active decision provider for the self-contained version. Principle prose is not silently translated into code. Rule revisions are attached to incident routing, and snapshots retain the configuration and pending next-day changes.
