# EasyMesh labs as a service

**Status:** Proposal. Nothing here is implemented. Every step must leave the
current way of working (a developer on the lab host, the suites, the local
room UI) exactly as it is.

**Prepared:** 26 September 2026, from the user's request of 25 September.

## 1. Goal

An optimizer developer who has no lab of their own develops and qualifies an
EasyMesh optimizer against our labs over the internet. They choose a lab
(RDK, prplMesh, and later the labs with OpenSync pods through EMOSA), a room
and an optimizer. Their optimizer observes the mesh and acts on it from their
own machine, using a Python library that gives them the primitives an
optimizer needs.

## 2. What exists today

| Piece | Where | What it offers now |
| --- | --- | --- |
| RDK optimizer | meta-cmf-bananapi-vcpe `gen/optimizer` | External Python process; observes em_cli's REST API (`/api/v1/topology`, `/clients`, `/devices`, `/bsses`, `/unassoc_sta_query`); steers through `gen/steer.sh`; normalized immutable snapshots, a pure decision engine, a hash-chained journal (`doc/easymesh/reference/optimizer/architecture.md`) |
| prplMesh optimizer | prplmesh-lab `optimizer` | The same architecture over prplMesh's NBAPI (ubus): topology, associated RCPI, Unassociated STA Link Metrics, `BTMRequest` |
| Room service | meta-cmf `gen/demo/room_demo` in each RDK lab VM (port 8891 in the VM, published on the host) | `/api/demo/*`: current state, worlds, apply a world, playback, interactions with a lease, RF observations, recording, optimizer safety (rate, failure and oscillation limits) and resume. **No authentication**; the service says so at start |
| Worlds | meta-cmf `gen/wmediumd/configurator` | Golden worlds (layout, walls, mobility, compiled links), pod variants (`worlds-pods`), a compiler (`wmdcfg`) to wmediumd |
| Suites | `run-easymesh-suite.sh rooms` (RDK), prplmesh-lab `tests` | The qualification a submitted optimizer would be held to |

Two facts shape the design:

- **The optimizer is already external.** Both labs run it as a separate host
  process that reads the controller's own interfaces and acts through the
  controller. Moving it off the host is a transport and authorization
  problem, not a redesign.
- **The two labs' native interfaces differ** (em_cli REST versus NBAPI over
  ubus) while the two optimizers normalize them into nearly the same snapshot.
  That normalized snapshot is the natural public contract.

## 3. Service model

```
 developer's machine                         lab host (rev120, ...)
 ┌───────────────────────┐   tailnet    ┌──────────────────────────────────────┐
 │ optimizer (their code)│  (WireGuard) │ lab gateway (new)                     │
 │  └─ easymesh-lab lib ─┼──────────────┼─► authn/z, lease, quotas, journal     │
 │ browser: room UI ─────┼──────────────┼─► room service proxy  ─► room_demo   │
 └───────────────────────┘              │   observation/action API ─► adapters │
                                        │     RDK: em_cli REST   prpl: NBAPI   │
                                        └──────────────────────────────────────┘
```

- **A lab session** is one developer holding the lease on one lab VM for a
  bounded time. The medium, the clients and the controller are shared state,
  so a lab VM serves one session at a time. Others queue.
- **The lab gateway** is one new process per lab host. It is the only thing
  reachable from outside. It authenticates the developer, holds the room
  lease on their behalf, forwards the room UI, exposes the observation and
  action API, enforces the safety limits server-side, and journals every
  request and outcome.
- **Selectable optimizer.** The room service already names its optimizer
  (`external-room-threshold-policy`). A session chooses one of: the lab's
  reference optimizer (as today), none (observe only), or **remote**, where
  the lab's own optimizer is paused and actions come only from the session.
  Whoever holds the lease is the only decision maker, as the architecture
  already requires of agent-local steering.

## 4. Transport

- **Tailscale** (WireGuard) as the common encrypted network: each developer is
  a tailnet node, each lab host a tagged node, and ACLs allow a developer to
  reach only the lab gateway port of the hosts they are granted. Nothing is
  published on the internet, and no lab host port other than the gateway's
  is reachable on the tailnet.
- Identity on top of the network: a per-developer token (or the tailnet
  identity headers of `tailscale serve`), checked by the gateway on every
  request. A token maps to a role: `view` (room UI read-only, observations),
  `act` (lease, actions, world changes).
- The gateway binds only to the host's tailnet address. The existing local
  ports (WebUI 21020, wmediumd console 21021, room 21022 on rev120) stay as
  they are for local use.

## 5. The API and the Python library

**API (versioned, JSON over HTTPS on the tailnet):**

| Group | Calls | Backed by |
| --- | --- | --- |
| Session | open, extend, close (restores the room's baseline), status, queue | new; the room service's lease and restore |
| Room | worlds, apply world, playback, movement, current state, RF observations | the room service API, proxied |
| Observe | snapshot (topology, BSSes, associations, serving RCPI with age), candidates (Unassociated STA Link Metrics per agent, with rejections), counters, events | RDK: em_cli REST; prpl: NBAPI; normalized as the optimizers do today |
| Act | steer(station, target BSSID), metric reporting policy, steering disallow lists | RDK: `steer.sh`/em_cli; prpl: `BTMRequest`; the safety gate before each |
| Outcome | per action: acknowledged, BTM status, association change, verified traffic, timeout | the optimizers' verifiers |
| Journal | the session's hash-chained journal, downloadable | the optimizers' journal format |

**Lab-specific first, standard later.** The first observation schema is the
labs' normalized snapshot, with each value's source and age, and marked
`simulated-radio` where it comes from hwsim (the prpl optimizer already
requires `--allow-simulated-candidates`). A later version maps it onto the
Broadband Forum's EasyMesh Data Elements (TR-181 `Device.WiFi.DataElements`),
so an optimizer written against Data Elements runs unchanged. The lab-specific
schema remains for what Data Elements do not carry (room ground truth, RF
generations, the lab's own health).

**Python library** (`easymesh-lab`, pip-installable, no lab code inside):

- `Lab.connect(url, token)`, `lab.session(room=..., optimizer="remote")` as a
  context manager that always closes and restores;
- `snapshot()`, `candidates(stations)`, `steer(sta, bssid)` returning an
  `Outcome` future, `set_policy(...)`, `events()` as an async iterator;
- primitives the reference optimizers already have, lifted out: freshness
  checks, hysteresis/dwell/cooldown state per station, candidate ranking, the
  journal writer, a replay harness over a downloaded journal;
- a skeleton optimizer (the threshold policy) as the starting point.

## 6. Safety and fairness

- The gateway enforces the existing safety limits (`/api/demo/optimizer/safety`:
  request rate, failure and oscillation windows, one action in flight per
  station) on every session, whatever the optimizer is.
- A lab is handed to a session only after its health gate passes (the room
  preflight: devices, radios, BSSes, associations, fresh metrics). The native
  labs drift (on 26 September the RDK gateway agent had stopped reporting
  client metrics until a policy change was pushed); a session must not start on
  a broken lab or be blamed for one.
- Session end, timeout or disconnect restores the room's baseline, as the
  room service does today on stop.
- Every request, response and outcome goes into the session journal, with
  the developer's identity. Nothing a session does touches another lab.

## 7. Room builder (later)

The world format already carries what a builder edits: AP and client
positions, walls with losses, mobility paths, and compiled links per
generation (`gen/wmediumd/configurator`). A browser editor would draw a floor,
place APs (native, pods) and clients, draw walls and paths, and submit the
result to the same compiler and checks (`build-goldens.py --check` style
validation, the compiler's link audit) before it may run. A second floor needs
a height dimension and floor losses in the compiler; that is a model change,
well after the editor.

## 8. Phases

Each phase ships only when the current local flow still passes its suites.

| Phase | Delivers | Done when |
| --- | --- | --- |
| 0 | Tailnet on one lab host (rev120), gateway skeleton with tokens and the journal; no lab access yet | A tailnet node reaches the gateway, nothing else on the host |
| 1 | **Remote room UI**: the room service proxied through the gateway, `view` and `act` roles, the lease held by the session | A remote browser runs a room walk; local use unchanged; lease conflicts refused |
| 2 | Observation API and the library's `snapshot()`/`candidates()` for the RDK lab | A remote script prints the same snapshot as the local optimizer at the same time |
| 3 | Actions and outcomes, `optimizer="remote"`, safety enforced at the gateway | The reference threshold policy, run remotely through the library, passes the RDK room catalog |
| 4 | The prplMesh adapter behind the same API | The same remote optimizer passes the prpl catalog |
| 5 | Session queue, per-developer quotas, journal download, replay | Two developers alternate without interfering |
| 6 | Data Elements mapping of the observation schema | A Data-Elements-only optimizer runs against both labs |
| 7 | Room builder | A drawn room compiles, passes the checks and runs |

## 9. Not in scope

- Running third-party code on our hosts. Optimizers run on the developer's
  machine; the lab only receives API calls.
- More than one session per lab VM at once.
- Physical radios. The labs are virtual RF; results are marked as such.

## 10. Open questions for the user

1. Who are the first users: in-house, partners, or open sign-up? This decides
   identity (tailnet sharing versus an identity provider) and quotas.
2. Should a remote optimizer also see the room's ground truth (true positions,
   model SNR), or only what a real controller sees? The first makes debugging
   easier; the second keeps it honest. Proposed: controller view by default,
   ground truth as an opt-in field marked as such.
3. Which hosts are service hosts? rev120 is dedicated to `rdk-emosa` today.
