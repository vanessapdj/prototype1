# School Robotics Operations prototype

A live browser simulation for MOE HQ to explore 24 school robot deployments. Each fictional school has two floor-cleaning and two toilet-cleaning robots. It calculates operations as the clock advances; it does not load the old recorded week.

## Open and try it

Open `index.html` with the `styles.css`, `js/`, `data/` and other folders beside it. The packaged offline fallback lets it work without a local preview server. On GitHub Pages it loads the canonical JSON data directly.

1. Leave School 01 selected and press **Start simulation**.
2. The simulation begins at 07:00. At the default speed the first toilet jobs start after a few seconds. Robot positions and progress are calculated live.
3. Around 07:58, two deliberate School 01 toilet interruptions demonstrate local recovery versus HQ escalation. The first can stay within school policy; the repeated fault goes to HQ.
4. Assign a supervisor, request vendor support or approve manual fallback. The robot does not immediately become healthy: the controller waits for simulated human support and reserves its time.
5. Use **Next work window** to advance through the day while still calculating all intermediate operations. Watch daytime preflight and the 20:00 floor dispatch. There is no replay timeline or pre-generated event file behind these controls.
6. Disable a lift, remove one operator from future allocations, hold new school dispatch or inject a robot stop. These change the ongoing simulation. Restore the scenario resource to see how the school responds.
7. Use **Save run** and **Restore saved run** to resume in the same browser. Export current state downloads a snapshot. Neither saving nor GitHub hosting makes the simulation continue while the page is closed.

## Edit principles and rules without changing code

Click **Principles & rules** in the toolbar. Edit principles, create or change condition/action routing rules, adjust recovery/access policy, and change staffing, schedules, durations, fault rates and battery assumptions. The current version is self-contained; no external AI service is required.

Principle wording records intent; structured rules implement behavior. Rule changes affect future decisions immediately. Schedule/staff/model changes apply next simulated day, or use **Start new run with these settings** to apply the whole configuration from the beginning. Existing assignments and booked durations are preserved. Changes have revisions and before/after records. Invalid settings are rejected before changing the run.

Applied settings persist in this browser. They do not automatically commit to GitHub or change another viewer's configuration. Use the Import / export tab to download `rules.json`, `principles.json` or `simulation.json` and upload the changed file under `config/` in GitHub. A settings bundle can transfer the configuration to another copy of the app. Browser-saved settings override repository defaults until replaced through the editor. The single-page edition also supports local settings and bundle import/export.

See [Editing rules](docs/editing-rules.md) for examples, supported facts and the timing of changes.

## Three columns and two audiences

| Column | MOE HQ job it supports |
| --- | --- |
| Left: observe | See the selected school's robot movement and resource context, scan all 24 schools, and inspect controller actions and their applied rules. |
| Middle: decide | Review exceptions outside local policy, assign ownership, arrange vendor or manual follow-up and request service-plan reviews. |
| Right: assess | Compare schools, monitor robot use within allowed operating windows, distinguish robot completion from manual fallback and inspect missed deadlines. |

Routine local issues should not all require HQ approval. Under the supplied default rules, the first routine staffed-shift interruption is routed to the school supervisor; other interruptions need HQ review. Those conditions and priorities are editable. A contractor plan review does not mark unfinished work complete. An access follow-up does not restore a lift: the scenario resource must separately become available again.

The future **cleaning supervisor** interface can reuse the school-scoped jobs, resources, incidents and Robot State objects. It should focus on that school's map, next task, local recovery and completion/reporting records. The current page is an HQ simulation, not an authenticated multi-role production system.

## Agents and AI

There are **24 independent `SchoolAgent` controller instances**, each with its own timetable, job queue, robots, day operators, lift, local metrics and incidents. One `HQSimulation` instance aggregates their observations and routes human decisions back to the relevant school.

These controllers apply explicit rules. **Gemini connects only when a visitor chooses Connect AI.** The activity feed reports rules and operational events; optional model advice is labelled separately in Human review. `agents/schools.json` defines the 24 school scopes for a future connected AI layer, and `schema/agent-proposal.schema.json` plus the agent instructions describe a recommendation boundary. These design files do not activate an AI service.

The chosen implementation is self-contained: no external AI service is needed. If that choice changes later, a model could interpret material exceptions through an optional server-side provider. It should not generate every movement or battery update. Models can share one underlying model while maintaining 24 separate school contexts; there is no need to train 24 models. A server must check school scope, observation freshness, allowed actions and required approvals before applying a model proposal. API credentials must not be placed in the public webpage or GitHub repository.

See `docs/architecture.md` for the self-contained architecture and the second audience. An external AI connection is not a prerequisite or outstanding task for this version.

## Files to maintain

| File | Edit it when… |
| --- | --- |
| `data/schools.json` | School timetables, building floors, operators or lift arrangements change. |
| `data/robots.json` | Robot assignments, identifiers or descriptive capabilities change. |
| `data/zones.json` | Pilot cleaning areas, geometry or area sizes change. |
| `config/simulation.json` | Shifts, cleaning rounds, windows, durations, rates or model assumptions change. |
| `config/rules.json` | Conditions, escalation routing, recovery/access rules or vendor hours/capacity change. |
| `config/principles.json` | Operating goals and guiding principles change. |
| `schema/stride-robot-state.schema.json` | The agreed Robot State profile changes. |
| `agents/schools.json` and agent instructions | A genuine AI connection and the agent scopes are implemented. |
| `js/simulator.js` | Live simulation behavior changes. |
| `js/dashboard.js` | HQ views and controls change. |
| `styles.css` and `index.html` | The interface layout changes. |
| `README.md` | Assumptions are validated or usage changes. |

Robot State output follows the project interpretation of the supplied STRIDE Robot State draft dated 23 October 2026. The schema is not an official STRIDE publication or certification. School jobs, staffing, timetable, incidents and metrics are separate ROAM concepts, not additional STRIDE fields. State can be inspected under each robot in the right column or via `simulation.getRobotState(robotId)`.

On a hosted page, the app reads the JSON files with caching disabled. For offline use after editing JSON, rebuild `data/bootstrap.js`:

```sh
python3 tools/build_bootstrap.py
```

That file is a generated fallback, not the place to maintain the source data. No Node package installation is needed to run the page.

## Publish on GitHub Pages

Upload the **contents of this folder** to the root of `vanessapdj/prototype1`, replacing the old recorded-replay `index.html`. Include at least `index.html`, `styles.css`, `js/`, `data/` and `config/`; retain the rest for documentation and validation. Upload extracted files, not the ZIP itself. The previous generated `sample-week` streams and Python replay are not required by this live app.

If Pages is configured to deploy from `main` and `/ (root)`, the site will use the new live page after GitHub's deployment finishes. The expected project URL is `https://vanessapdj.github.io/prototype1/`; this package does not itself confirm a successful deployment.

## Time and scheduling

The first horizon is seven calendar days starting 4 January 2027. Two years is 731 days. Start/Pause and the speed controls advance an integer-minute simulation; the setting **Two years in one real day** targets 731x real time. Browsers may throttle background tabs or a sleeping computer, so this is not a guaranteed wall-clock completion time. Use a persistent backend for unattended execution.

Toilet robots run only in the staffed 07:00–16:00 window. Preparation, transfer and post-cleaning care consume operator time. Operators cannot be double-booked or assigned a task crossing their break or shift end. There are three toilet rounds and two pilot blocks per robot, on its home floor.

Floor robots require day preflight, a simulated site-vacancy release and their allowed night window. They share one lift per school and return to dock. Office/staff-room floor jobs are scheduled on Tuesday and Friday from 22:00. Restoring a night fault in daytime leads to simulated manual completion of the remaining task; floor robots do not simply resume in an occupied daytime window.

Every school has a synthetic timetable, with different closing windows. A routine clock-based release is not proof of actual vacancy or permission to operate a real robot.

## Measures

- Robot use = cleaning minutes divided by elapsed robot-minutes in permitted operating windows. Floor robots are not penalised for daytime hours when they are not scheduled to run.
- Robot job completions and simulated manual completions are separate. Neither is an independent cleanliness audit.
- Missed deadlines remain counted even when work is later completed.
- Jobs planned so far include later jobs in the current day. This is not a percentage of all work due already completed.
- Human minutes cover modeled robot support and fallback only. They exclude other cleaning duties and continuous technician attendance, so they are not a savings estimate.
- Cumulative metrics persist in snapshots. Old closed job records and event-feed entries are trimmed to keep the browser manageable; exported state is not a complete historical event archive.

## Scope and assumptions

All school names, geometry, capacities and failure rates are fictional. School calendars have synthetic weekdays only, without official MOE terms, holidays, examinations or actual room bookings. Each school has two modeled day operators supporting robots, not a complete cleaning workforce. Four toilet blocks are pilot coverage, not the full school's toilets. Office jobs use the floor robots, not extra robots.

Battery charge and cleaning draw are simplified. Tank capacities are descriptive and fluid consumption is not modeled. No certified safety logic, route collision avoidance, chemical dwell time, comprehensive manual cleaning, premises-wide periodic maintenance, live vendor API or physical lift control is present. Descriptive capability fields do not imply vendor certification. Random faults are seeded and illustrative, not a forecast of measured reliability.

The initial policy assumes touchpoint support rather than a technician continuously observing every toilet robot. Shared vendor support capacity is a simple one-ticket-at-a-time model per fictional vendor within a daytime window, with an operator still required. This is an operating-model hypothesis to test.

The school-cleaning patterns were informed by the [NEA school sanitation template](https://www.nea.gov.sg/docs/default-source/our-services/public-cleanliness/es-regime/environmental-sanitation-programme-for-specified-schools-4th-edition.docx). Exact robot times, assignments and performance are simulation choices, not prescribed robot operating arrangements.

## Tests

With Node.js available:

```sh
node tests/simulator.test.cjs
node tests/dashboard.test.cjs
node tests/policy.test.cjs
node tests/editor.test.cjs
```

The tests cover independent school state, genuinely live position changes, local versus HQ escalation, delayed human intervention, lift and operator scenarios, operating windows, bounded battery/utilisation, save/restore and dashboard control logic. Robot State objects were also checked against the project STRIDE schema with date-time/UUID validation. Browser visual QA has not been completed; no browser preview was attempted after the earlier declined permission.

## Optional Gemini connection

Click **Connect AI**. Each visitor enters their own Gemini API key, confirms that their Google AI Studio project shows Free Tier with paid billing off, then clicks **Connect & test**. This makes one small real generation request. A successful response is shown as connected; listing a key or entering it alone is not a successful test. You do not need to give the developer a key.

Once an exception reaches Human review, choose **Ask AI for advice**, then **Ask Gemini**. The simulation pauses and sends the selected fictional school's exception, relevant state and current editable settings to Google. Gemini's recommendation and snapshot evidence appear in the middle panel. The human still chooses an existing action button. Advice never runs robot commands or overrides rules. Changed state/rules invalidate a pending reply; older accepted advice is labelled as an earlier snapshot. The 24 controllers remain rule-based; this addition provides on-demand AI advice, not 24 autonomous model agents.

Keys remain in page memory, are not written to browser storage, exports or repository files, and disappear on reload or disconnect. Each visitor has a separate connection. Browser-side personal-key entry is a prototype pattern; a future shared organisational connection needs a server to protect its credentials. No owner key is embedded here.

Google decides model availability, free eligibility, quotas and charges. ROAM cannot inspect your billing tier or guarantee zero cost for an incorrectly configured paid project. The reviewed model is Gemini 2.5 Flash-Lite (standard). It does not switch models automatically. At most 10 generation attempts per page visit, at least 15 seconds apart, including test attempts. No retries run automatically. Access/quota rejection disconnects AI while preserving the rules simulation. Reconnecting does not reset the limit. Reloading starts a new visit; this local limit is not a provider-wide cost or quota control.

Only fictional demo data should be used. Free-tier submissions may be used by Google to improve products. Review [Google pricing](https://ai.google.dev/gemini-api/docs/pricing), [API key guidance](https://ai.google.dev/gemini-api/docs/api-key) and your own project's limits before connecting. No key or live paid request was used in development. Automated connection tests use mocked responses; live API compatibility and browser visual QA remain unverified.

Connection implementation: `js/gemini.js` (provider and limits), `js/connection.js` (screen and scoped advice). The legacy `schema/agent-proposal.schema.json` remains future autonomous-agent scaffolding; this manual-advice adapter validates its own smaller recommendation/evidence contract and executes no proposals.
