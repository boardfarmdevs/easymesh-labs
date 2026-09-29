# Alignment plan: towards EMOSA in the router

Agreed 2026-09-28. The end point of this plan is being **ready to start carrying
EMOSA (in C) optionally in the RDK gateway image** (`bpibroadband`), where it
becomes part of the router. Carrying it is the step after this plan; it waits
until the labs below are aligned.

## Where each project stands in the alignment

| Project | Role | Changes in this plan |
| --- | --- | --- |
| opensync-lab | OpenSync with the mv3 router: learning, and the source of the OpenSync pod image | none, except that the pod image the EMOSA labs use is pinned |
| easymesh-lab | The physical protocol lab: EasyMesh on a certified extender, learning | none |
| meta-cmf-bananapi-vcpe | The RDK optimizer lab | a wired extender next to the four Wi-Fi extenders, fully in the room tests; EMOSA as an option of the lab |
| prplmesh-lab | The prplMesh optimizer lab | the same wired extender; EMOSA as an option later |
| emosa-lab | EMOSA development, the reference EMOSA suite and deep qualification | the Python original and the C implementation interchangeable behind identical interfaces |

Two rules follow. The optimizer labs get the wired extender whether EMOSA is
present or not. EMOSA in an optimizer lab is a configuration of that lab: the
EMOSA container, the pods' gateway (GTP) and at least two OpenSync pods that
host clients in the rooms.

## Phases

Order: 0, then 1, then 3; 2 and 4 alongside. Status is kept here as the work
goes.

### Phase 0: freeze the current reference (rev120)

| Step | Done when | Status |
| --- | --- | --- |
| 0.1 Close the EMOSA 24-room qualification | the 239f9f6 images deployed in `rdk-emosa`, the pods-wired suite run once, emosa-lab `doc/architecture/rdk-lab.md` §8 steps 3 to 5 marked done | done (29 Sep): the pods-wired suite on the 239f9f6 images, eight steps of nine, the catalog 24 of 24; geometry alone passed its three rooms (emosa-lab `rdk-lab.md` §8) |
| 0.2 Operational steps out of the VM | the image redeploy order and the room-settled wait are in meta-cmf-bananapi-vcpe, not only in `rdk-emosa`'s `/root` (the other `/root` scripts are diagnostics) | done: meta-cmf-bananapi-vcpe `gen/lab-redeploy.sh` (37177e6); the room waits are `gen/lab-bringup.sh room` and `status` |
| 0.3 Every input pinned | `manifest.json` also pins the OpenSync pod image the EMOSA labs run (stamp and opensync-lab commit) | done: `images` in `manifest.json` (the pod image is opensync-lab daca9a9) |
| 0.4 The configurations as they are | [lab-configurations.md](lab-configurations.md) lists every stage of the RDK lab + EMOSA and only the gaps still open | done |

### Phase 1: a wired extender in the RDK optimizer lab (meta-cmf-bananapi-vcpe, no EMOSA)

| Step | Done when | Status |
| --- | --- | --- |
| 1.1 The lab owns its wired LAN port | the lab's build makes the bridge into the controller's LAN (today `br-emosa`, made by emosa-lab) and the wired extender (`bpiap-004`), in the order `gen/wired-extender.sh` keeps | done: `gen/wired-extender.sh lanport`, build stage `56-wired-extenders.sh` (`EASYMESH_WIRED_EXTENDERS`, default 1), started with the Wi-Fi extenders and checked after the medium, counted by the health audits; `rdk-0929` built from scratch with it |
| 1.2 A backhaul parent | the wired extender's APs are on the medium, so Wi-Fi extenders can take it as their parent; its backhaul station stays down and no L2 loop forms | in part: rdk-wifi-hal 0045 keeps its station from ever connecting, and a guarded wired extender has RF to the mesh. Open: RDK's extender mode does not act on an Ethernet uplink, so its own backhaul BSS stays down and its `brlan0` gets no DHCP address; `backhaul-wired-parent` fails until it does |
| 1.3 The standard rooms with it | the lab's own world set has the wired extender (`extender_5`) in every room, same world IDs; the set without it stays only as the historical baseline | done: `worlds-wired`, selected by the lab's own room drop-in wherever it has a wired extender; the suite takes the set from the room |
| 1.4 Topology checks include it | the controller's tree and em_cli show it as a wired child of the gateway, and the branch and star checks accept Wi-Fi extenders under it | done: an Ethernet child of the gateway, never a Wi-Fi child, in the acceptance and the health audit; the geometry rooms read it |
| 1.5 Rooms about it | client steering onto and off it, a backhaul parent handover to it, its loss and recovery | done for steering onto and off it and its loss and recovery (per-room expected APs, all passed on `rdk-0929`); the parent handover to it (`backhaul-wired-parent`) waits for 1.2 |
| 1.6 From scratch | a fresh RDK lab VM with 4 Wi-Fi and 1 wired extender, from new images, passes the full suite; it is the optimizer lab | done (29 Sep): `rdk-0929` on rev140 from the 0045 images; the catalog passed all 27 rooms (fifty-client-counter-roam on a rerun), the three standard geometry rooms pass with the wired extender present, world-switch and restore-default passed |

### Phase 2: the same for prplMesh (prplmesh-lab)

| Step | Done when | Status |
| --- | --- | --- |
| 2.1 A wired prplMesh agent | the lab makes a wired extender on its controller's LAN | in progress: `prpl-agent-05` on the backhaul network, no backhaul station (prplmesh-lab 17de2de); fresh VM pending |
| 2.2 Rooms and checks | the prplMesh rooms have it, with the same topology, steering and recovery checks as the RDK lab | in progress: `worlds-wired`, the wired checks, expected APs and the geometry probe ported (17de2de, 4847a6a); fresh VM pending |
| 2.3 From scratch | a fresh prplMesh VM on a host other than rev120 passes the full suite | |

### Phase 3: EMOSA as an option of the RDK lab (after phase 1)

| Step | Done when | Status |
| --- | --- | --- |
| 3.1 Ownership | meta-cmf-bananapi-vcpe: the option and the pod room set; emosa-lab: the adapter and its deploy stage on the lab's LAN port; opensync-lab: the pinned pod image | |
| 3.2 One entry point | one script turns the option on: EMOSA, fleet, GTP, two pods, telemetry, backhaul, rooms | |
| 3.3 Two room sets | the standard set (4 + 1) and the standard set with pods; the separate pod and pod-wired sets are merged away | |
| 3.4 Open items | the pods' backhaul in the geometry rooms (EMOSA takes an extender as its parent); decided whether the pods' fronthaul is more than 2.4 GHz | |
| 3.5 From scratch | a fresh RDK lab with the option on passes the full suite with the pods; it replaces `rdk-emosa` | |

### Phase 4: Python and C interchangeable (emosa-lab, can start any time)

| Step | Done when | Status |
| --- | --- | --- |
| 4.1 The C gaps closed | telemetry (unassociated station metrics from probe reports), uplink (the switch to the Wi-Fi backhaul), periodic AP metrics and associated station metrics, a durable journal | |
| 4.2 Vectors for every behaviour | every behaviour the rooms rely on, and every suite finding, has vectors; both implementations pass all of them | |
| 4.3 Swapped as is | the reference suite, and the RDK pod suite with both pods on C and with one of each, give the same results as with Python | |

### Phase 5: ready to carry EMOSA in the gateway

Design and evidence only; carrying it starts after this.

| Step | Done when | Status |
| --- | --- | --- |
| 5.1 1905 on the router | EMOSA's virtual agents (their own AL MACs) next to the gateway's own 1905 daemon and agent on `brlan0`: decided | |
| 5.2 The GTP role | the router serves the pods' onboarding and ends their GRE, or supports only the Wi-Fi backhaul and Ethernet pods: decided | |
| 5.3 How pods find EMOSA | the fleet's front port and the redirect on the router's LAN: decided | |
| 5.4 Footprint | the C EMOSA's memory and CPU measured against the gateway container's limit (1 GiB, already tight) | |
| 5.5 Recipe design | an opt-in feature of the layer, off by default: the default image unchanged | |
| 5.6 Code policy | the C implementation is a lab prototype; the path to production code (the board's rule on AI-written code) decided | |

**Gate to start carrying EMOSA in the gateway:** phases 1, 3 and 4 done, phase
2 done or deferred on purpose, and the decisions of phase 5 made.

## Hosts

| Host | In this plan |
| --- | --- |
| rev140 | Yocto builds; the fresh RDK optimizer lab (phase 1.6) |
| rev120 | `rdk-emosa` (phase 0; replaced in phase 3.5) and the physical protocol lab |
| rev150 or rev140 | the fresh prplMesh lab (phase 2.3); never rev120 |
