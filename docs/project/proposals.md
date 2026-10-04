# Proposals register

[Documents](../README.md)

**Kind:** project. Every proposal of the labs, wherever it is kept, with a decision on it.
**Started:** 2 October 2026, from the [project assessment](assessment.md) (its item 3).

A proposal stays in the repository whose subject it is; this register is the one place
that lists them all and says what is decided. The repositories are linked by their sites;
each proposal's path is given in that repository.

## Statuses

| Status | Meaning |
| --- | --- |
| **chosen** | the route to follow when there is capacity; the next step is named |
| **open** | written, not yet decided |
| **parked** | decided not now; kept for later, with the reason |
| **retired** | superseded; the text is in the repository's history |

## The register

| Proposal | Where | Prepared | Status | Decision and next step |
| --- | --- | --- | --- | --- |
| Pluggable optimizer algorithms | [easymesh-optimizer](https://vcpe.dev/easymesh-optimizer/) `docs/proposals/algorithm-plugins.md` | 2 Oct | **chosen** (2 Oct) | the first route for optimizer work from outside: an algorithm as a plugin, today's policy the default. Next: stages 1 and 2 |
| The optimizer workbench | [easymesh-optimizer](https://vcpe.dev/easymesh-optimizer/) `docs/proposals/optimizer-workbench.md` | 29 Sep | **chosen** (2 Oct), later | the detailed design of the plugins' stages 3 to 5 (sandboxed process, uploads, queue, scorecard). After plugin stage 2 |
| Remote labs | [easymesh-remote](https://vcpe.dev/easymesh-remote/) `docs/proposals/remote-labs.md` | 2 Oct | **chosen** (2 Oct) | access to every lab; a prerequisite of outside work of any kind. Next: step 2, a lab's interfaces read from its VM |
| EasyMesh labs as a service | this repository, [labs-as-a-service.md](../proposals/labs-as-a-service.md) | 26 Sep | **parked** (2 Oct) | the API route, in which a developer's code stays outside and drives a lab; the alternative to plugins. Its access part is remote labs, its Data Elements part the application proposal's |
| The optimizer as an application | [easymesh-optimizer](https://vcpe.dev/easymesh-optimizer/) `docs/proposals/optimizer-as-an-app.md` | 2 Oct | open | the one place for a Data Elements view of the controller; the workbench's version 2 contract and labs as a service defer to it. An experiment, later |
| More capable clients | [easymesh-clients](https://vcpe.dev/easymesh-clients/) `docs/proposals/more-capable-clients.md` | 2 Oct | open | a contract, actions, models, behaviours; steps 1 and 2 are small |
| Client models | [easymesh-clients](https://vcpe.dev/easymesh-clients/) `docs/proposals/client-models.md` | 29 Sep, revised 3 Oct | **chosen** (3 Oct); **built on a bench** (3 Oct) | models of devices (iPhone, iPad, Mac, Pixel, Galaxy, Windows with Intel, iwd) from their documented roaming, on one wpa_supplicant 2.12 build with three patches. Built in easymesh-clients with a bench of simulated radios on the labs' medium: 441 runs, every conformance test of every model passed (`docs/records/bench-2026-10-03`). No lab uses it yet. Next: one lab takes the build, first 2.12 as today's client with that lab's suite, then one model by hand in a room. It closes the realism gap the assessment names (item 2, R3) |
| EMOSA's product apart from its lab | this repository, [emosa-product-split.md](../proposals/emosa-product-split.md) | 1 Oct | open | for the handover (alignment plan 8.6) |
| A retail EasyMesh extender | [meta-cmf-bananapi-vcpe](https://vcpe.dev/meta-cmf-bananapi-vcpe/) `docs/proposals/retail-easymesh-extender.md` | 25 Sep | open | an experiment with real hardware on the RDK lab's controller |
| Neighbor-network rooms | [easymesh-medium](https://vcpe.dev/easymesh-medium/) `docs/proposals/neighbor-rooms.md` | 9 Sep | open | rooms with a neighbouring network's interference |
| Rooms: design and plan | meta-cmf-bananapi-vcpe, `docs/proposals/rooms-convergence.md`, removed | 29 Sep | **retired** (2 Oct) | its phases 0 to 2 were done another way by the splits of 30 September; its phase 3 is remote labs' steps 2 and 3; its phases 6 to 8 are the workbench. Two ideas are parked below |
| The room builder inside each lab | from the rooms plan, phase 4 | 29 Sep | **parked** (2 Oct) | the builder served by each lab VM at `/builder/`, publishing rooms into a session tree beside the golden rooms, never into the suites. After remote labs step 3 |
| The Pages sites as an offline playground | from the rooms plan, phase 5 | 29 Sep | **parked** (2 Oct) | each public site says it is offline, and its build refuses a lab address or a live viewer mode (the RDK lab's explorer build already refuses a live viewer) |

## Overlaps, resolved

- **Optimizer work from outside the team.** Plugins (the code comes into the lab) are
  chosen; labs as a service (the code stays outside, behind an API) is parked as the
  alternative. Remote labs gives both their access; the workbench is the plugins' later
  stages.
- **A Data Elements view.** Three proposals had one. The application proposal owns it; the
  others defer to it.
- **The clients.** Client models is step 3 of more capable clients, in one repository.

## Keeping it

- A new proposal gets a row here when it is written, and starts **open**.
- A subject that already has a proposal is extended, not given a second one.
- A decision changes the status and the date in this table; the proposal itself says the
  same in its status line.
- A proposal that is implemented leaves this register; its project's plan or state section
  carries it from then on.
