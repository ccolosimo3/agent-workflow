# Assignment And Status Formats

## Orchestration Assignment

```text
Orchestration assignment
- program / work item / assignment generation:
- role and terminal deliverable:
- base SHA / branch / checkout:
- owned paths / forbidden paths:
- dependencies and frozen inputs:
- done criteria:
- worker-owned verification / coordinator-owned verification:
- environment attestation:
- allowed / ask / forbidden delta:
- route class / exact model / reasoning / policy revision / rationale:
- active leases and prohibited shared state:
- heartbeat and inspection contract:
- terminal report path and required fields:
```

## Worker Terminal Report

```text
Outcome: complete | blocked | approval-needed | failed
Assignment generation:
Owned-path changes:
Current tip / dirty state:
Commands and exact results:
Unrun or delegated gates:
Approval/live/paid/destructive attempts:
Review state and reviewer task ID:
Blocker and one diagnostic already attempted:
Next safe action:
```

## Operator Status

```text
Outcome/phase: <program state and current candidate>
Completed: <converged work items and exact evidence>
In flight: <owner task, assignment generation, current gate>
Blocked/decision: <exact operator/environment need, or none>
Safety/spend: <live/paid/destructive attempts and actual amount>
Next: <next safe critical-path action and why>
Estimate: <remaining gates/review cycles, or unknown with reason>
```

