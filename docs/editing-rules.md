# Editing operating principles and rules

The prototype is self-contained and rule-driven. No external AI service is required to change its operating model. Click **Principles & rules** in the dashboard toolbar.

## Principles

Edit, enable, disable, add or remove statements such as “prioritise closing the unmet cleaning demand” or “make human support effort visible.” Enabled principles are shown in the dashboard. They explain intent and are recorded in revisions. Their wording is not interpreted as executable code: use the rule and setting controls to change behavior.

## Decision rules

Create condition/action rules using observed simulation facts. Each rule has a name, enabled flag, priority, a set of conditions and a route to the local supervisor or HQ. Rules are evaluated in ascending priority order; the first matching enabled rule wins. Conditions within one rule are combined with AND. Use several rules for alternative combinations. An empty condition list always matches. Unmatched interruptions go to HQ.

For example, the initial local-recovery rule requires:

- Within staffed shift equals Yes.
- Operators on shift greater than 0.
- School faults today less than 2.
- Exception type equals `robot_stopped`.

Change the last value to 5 if you want the first four same-day interruptions to remain local. Disable that rule, or disable local routing, to request HQ review instead. This is configuration data, not a fixed second-fault condition in the engine.

Rules can use exception type, staffed-shift status, operator counts, the school's fault count, robot type, task progress, deadline status and reported cause. The current engine supports these facts and local/HQ coordination actions. New facts or fundamentally new robot capabilities still require an engine feature; this is not an arbitrary-code editor.

Changing a route does not create staff or instantly recover a robot. Resource and operating-window checks still apply.

## Scenario settings

Common assumptions have ordinary fields: staffing levels (including zero operators), shifts and breaks, toilet rounds, office weekdays, floor windows, preparation/recovery time, productivity, battery assumptions and seeded fault probabilities.

Execution rules also control whether toilet cleaning needs a staffed shift, floor dispatch needs vacancy/preflight, lift escalation time, fault-assessment progress, outside-window recovery policy and vendor capacity/hours.

School-specific timetables remain editable in `data/schools.json`. A school's later vacancy release is combined with the global earliest release. The global field cannot pretend a school with a later timetable is already vacant.

The current version supports a same-day staff shift and toilet window, an overnight floor window and office jobs inside the shared floor window. The editor rejects inconsistent settings with an explanation.

## When changes take effect

**Apply rules · queue schedule changes** applies principles and decision/execution/vendor rules to future decisions immediately. Existing assignments stay assigned. Schedule, staffing and physical-model parameters are queued for the next simulated day, before new daily jobs are created. Already-booked human work and current job durations finish under their existing reservations.

**Start new run with these settings** applies the full edited configuration from the beginning. A snapshot of the prior run is retained in browser storage. The Import / export tab can restore that prior run. Start-date and default-horizon changes require this explicit new-run action rather than changing the calendar beneath an active run.

Changes include a revision and a field-level before/after record. Incidents identify the routing rule and revision used when they were created. New rules do not retroactively rewrite those records.

## Save and maintain in GitHub

Applied settings are saved in this browser and loaded when this page is reopened. A banner identifies browser-saved settings. These edits do not automatically change the public GitHub repository or another person's view.

For the maintainable project:

1. Open the Import / export tab.
2. Download `rules.json`, `principles.json` and/or `simulation.json` after validating your edits.
3. Upload the changed files into the repository's `config/` folder, replacing the previous versions.
4. GitHub Pages reads those canonical JSON files when it loads. Existing browser-saved settings can be compared or replaced using **Load repository settings into editor**, then Apply.

For the single-file edition, browser edits persist locally. Export a settings bundle and import it into another copy of the app to transfer the settings. Uploading an unchanged single HTML file does not embed subsequent browser edits. Use the maintainable project and canonical JSON files for shared GitHub configuration.

The settings bundle includes all three layers and can be imported without writing code. An advanced JSON view exposes fields not represented by the common form, such as specific demonstration scenarios and calendar date overrides. Invalid bundles are rejected before changing the running world. No executable scripts are evaluated from rule values.
