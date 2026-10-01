# Alignment plan: towards EMOSA in the router

Agreed 2026-09-28. The end point of this plan is being **ready to start carrying
EMOSA (in C) optionally in the RDK gateway image** (`bpibroadband`), where it
becomes part of the router. Carrying it is the step after this plan; it waits
until the labs below are aligned.

## Where each project stands in the alignment

| Project | Role | Changes in this plan |
| --- | --- | --- |
| opensync-lab | OpenSync with the mv3 router: learning, and the source of the OpenSync pod image | none, except that the pod image the EMOSA labs use is pinned |
| easymesh-lab | The physical protocol lab: EasyMesh on certified extenders, learning | none |
| meta-cmf-bananapi-vcpe | The RDK optimizer lab | a wired extender next to the four Wi-Fi extenders, fully in the room tests; EMOSA as an option of the lab |
| prplmesh-lab | The prplMesh optimizer lab | the same wired extender; EMOSA as an option later |
| emosa-lab | EMOSA development, the reference EMOSA suite and deep qualification | the Python original and the C implementation interchangeable behind identical interfaces; the C taken to production quality (phase 8) |
| easymesh-medium (new, phase 6) | The RF medium: wmediumd, hwsim, the configurator and its rooms, the observer and console | one home for the medium both optimizer labs use; today two diverging copies in meta-cmf-bananapi-vcpe and prplmesh-lab |

The project rests on two core components: **the RF medium** (wmediumd emulating
the radio medium correctly, for every lab) and **EMOSA** (the full conversion
between OpenSync's OVSDB and EasyMesh). Each gets one repository with its own
specification and tests; the labs, the room tooling and the learning projects
consume them.

Two rules follow. The optimizer labs get the wired extender whether EMOSA is
present or not. EMOSA in an optimizer lab is a configuration of that lab: the
EMOSA container, the pods' gateway (GTP) and at least two OpenSync pods that
host clients in the rooms.

## Phases

Order: 0, then 1, then 3; 2 and 4 alongside (all done 29 Sep). Then 6 (the
medium), 7 (documentation) and 8 (EMOSA C to production); 5's remaining
decisions alongside; 9 after 8. Status is kept here as the work goes.

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
| 1.2 A backhaul parent | the wired extender's APs are on the medium, so Wi-Fi extenders can take it as their parent; its backhaul station stays down and no L2 loop forms | done (29 Sep): rdk-wifi-hal 0045 keeps its station from ever connecting, and a guarded wired extender has RF to the mesh. OneWifi never started its own 5 GHz backhaul BSS (in EasyMesh node mode it starts only the station, and the controller's settings match what it stored); its unit brings it up and gives its `brlan0` an address from the gateway (meta-cmf f5ad0b2), also after a reboot. On `rdk-0929`, `backhaul-wired-parent` passed: a Wi-Fi extender took the wired extender as its parent |
| 1.3 The standard rooms with it | the lab's own world set has the wired extender (`extender_5`) in every room, same world IDs; the set without it stays only as the historical baseline | done: `worlds-wired`, selected by the lab's own room drop-in wherever it has a wired extender; the suite takes the set from the room |
| 1.4 Topology checks include it | the controller's tree and em_cli show it as a wired child of the gateway, and the branch and star checks accept Wi-Fi extenders under it | done: an Ethernet child of the gateway, never a Wi-Fi child, in the acceptance and the health audit; the geometry rooms read it |
| 1.5 Rooms about it | client steering onto and off it, a backhaul parent handover to it, its loss and recovery | done: client steering onto and off it and its loss and recovery (per-room expected APs), and the parent handover to it (`backhaul-wired-parent`), all passed on `rdk-0929`; the four geometry rooms passed in one run (29 Sep, the browser on rev150) |
| 1.6 From scratch | a fresh RDK lab VM with 4 Wi-Fi and 1 wired extender, from new images, passes the full suite; it is the optimizer lab | done (29 Sep): `rdk-0929` on rev140 from the 0045 images; the catalog passed all 27 rooms (fifty-client-counter-roam on a rerun), the three standard geometry rooms pass with the wired extender present, world-switch and restore-default passed |

### Phase 2: the same for prplMesh (prplmesh-lab)

| Step | Done when | Status |
| --- | --- | --- |
| 2.1 A wired prplMesh agent | the lab makes a wired extender on its controller's LAN | done: `prpl-agent-05` on the backhaul network, no backhaul station (prplmesh-lab 17de2de); `prpl-0929` built on rev140 with it; the expanded acceptance and the optimizer check pass with six devices (17928c2) |
| 2.2 Rooms and checks | the prplMesh rooms have it, with the same topology, steering and recovery checks as the RDK lab | done: `worlds-wired`, the wired checks, expected APs and the geometry probe (17de2de, 4847a6a, 89e1304); the room fixed for a sixth AP (client RF limit, RF beyond one control frame, wmediumd 0036, the world catalog kept, a fair session lock) |
| 2.3 From scratch | a fresh prplMesh VM on a host other than rev120 passes the full suite | done (29 Sep): `prpl-0929` on rev140 from scratch; acceptance and optimizer check passed with six devices, the catalog 26 of 27 (`band-upgrade-24-5` passed alone), the four geometry rooms (`backhaul-isolation-recovery` for the first time, `backhaul-wired-parent`, the handover on a rerun), static, WebUI and browser sections; the browser on rev150 (prplmesh-lab `docs/current-state.md`) |

### Phase 3: EMOSA as an option of the RDK lab (after phase 1)

| Step | Done when | Status |
| --- | --- | --- |
| 3.1 Ownership | meta-cmf-bananapi-vcpe: the option and the pod room set; emosa-lab: the adapter and its deploy stage on the lab's LAN port; opensync-lab: the pinned pod image | done: meta-cmf owns the option (`build.sh emosa`, `EASYMESH_EMOSA=1`, 37e181d) and the pod room set (b922dfb); emosa-lab owns the steps on the lab's LAN port (`deploy/rdk-lab/lab.sh stage`, `lab.sh up`, 10ccb53); the pod image is pinned in `manifest.json` |
| 3.2 One entry point | one script turns the option on: EMOSA, fleet, GTP, two pods, telemetry, backhaul, rooms | done: `EASYMESH_EMOSA=1 gen/vm/lxd/build.sh build` built `rdk-emosa-0929` on rev120 in one command, the lab and then the whole option (`lab.sh up`), 29 Sep; `build.sh emosa` does the same on an accepted VM |
| 3.3 Two room sets | the standard set (4 + 1) and the standard set with pods; the separate pod and pod-wired sets are merged away | done: `worlds-pods` is the standard rooms (with the wired extender) plus the pods, all 31 worlds; `worlds-pods-wired` and its manifest are gone (meta-cmf b922dfb, emosa-lab 10ccb53) |
| 3.4 Open items | the pods' backhaul in the geometry rooms (EMOSA takes an extender as its parent); decided whether the pods' fronthaul is more than 2.4 GHz | done (29 Sep): EMOSA carries out Backhaul Steering (emosa-lab 615341b, a924b26) and the RDK controller's `SteerWiFiBackhaul()` now sends it (unified-wifi-mesh 0232, meta-cmf 96188ea; upstream it was a stub). In the geometry rooms the pods' stations follow the room, and the room moves each pod to its strongest native AP before a room's RF applies (meta-cmf 2ce8fba to e08aaca): on `rdk-emosa-0929` the four geometry rooms passed with the pods moved onto extender_1, extender_2 and the wired extender. Decided: the pods' fronthaul stays 2.4 GHz in this plan, because an EMOSA agent is one radio (spec §9) |
| 3.5 From scratch | a fresh RDK lab with the option on passes the full suite with the pods; it replaces `rdk-emosa` | done (29 Sep): `rdk-emosa-0929` on rev120, built from scratch with the option on, replaces `rdk-emosa` (stopped, kept as snapshot `before-replacement-20260929` until deleted by hand). Its room suite with the pods: guest audit, default readiness, the RF hover, access and property rooms, the switch through all 31 worlds and the return to the default passed; the catalog (25 of 27, both the browser's load on rev120) and the geometry rooms were run again whole with the browser on rev150: the catalog 27 of 27, the four geometry rooms with the pods moved onto extender_1, extender_2 and the wired extender. The first geometry room's pods onboard again whenever their native extender re-parents, so a room with pods gets the 150 s branch window (meta-cmf 82704f1; emosa-lab `rdk-lab.md` §9) |

### Phase 4: Python and C interchangeable (emosa-lab; the evidence also in the RDK lab)

The work is emosa-lab's (`c/`, the vectors in `spec/conformance`). The swap
itself is emosa-lab's `lab.sh agent POD python|c`; 4.3's evidence runs in the
RDK lab with the EMOSA option.

| Step | Done when | Status |
| --- | --- | --- |
| 4.1 The C gaps closed | the C agent does what the Python agent does (the list in emosa-lab `c/README.md`, and what phase 3 added): the telemetry scope (AP metrics from the pod's statistics, unassociated station metrics from probe reports, the probe watch on `Band_Steering_Clients`); the uplink scope (the switch to the Wi-Fi backhaul, the Backhaul STA Capability Report of the pod's station); **Backhaul Steering** carried out as the Python agent does (615341b, a924b26), its answer kept across a session renewal (today C refuses every request, and the geometry rooms with pods depend on it, 3.4); Link Metric and AP Metrics answers; retries of the Early AP Capability Report; the durable journal; schema validation of the configuration and status | done (29 Sep): emosa-lab `c/` has the journal, secret store and operation engine (Store-compatible, so either agent takes over a pod's state directory), the AP, telemetry, steering, probe watch and uplink scopes, AP metrics from the pod's statistics, Link Metric and AP Metrics answers, Backhaul Steering kept across a session renewal, the Early AP Capability Report retries, the kept channel and Multi-AP policies, schema validation of config and status, and the session timing of the Python agent (discovery, back-off, renewals, client re-announcement) (2c74ffe..e3a5133). Known differences in `c/README.md`: the report source's token, and the fleet stays Python |
| 4.2 Vectors for every behaviour | every behaviour the rooms rely on (Backhaul Steering across a session renewal among them), and every suite finding, has vectors; both implementations pass all of them | done (29 Sep): 19 vector sets in `spec/conformance`, the reference reproduces all of them (`tests/test_conformance.py`) and C replays 677 checks with none failing (`emosa-vectors`). Added for phase 4: metrics, backhaul-steering (across a session), scope-writes, engine, early-report, steering-queue, probe-watch, session-timing; the suite findings among them: no M2 after M1, the silent controller in any state, the unserved pod, the pod dropped with its extender (a new source), Backhaul Steering across a renewal, the client re-announcement after a controller restart, the stations' ages taken as of each Topology Response |
| 4.3 Swapped as is | the reference suite (emosa-lab), and the RDK room suite with the pods (meta-cmf `run-easymesh-suite.sh rooms` on the RDK lab with the EMOSA option) with both pods on C and with one of each, give the same results as with Python; the evidence records which implementation each pod ran (the C agent's status says `c-lab-prototype`). Wanted, not required: a build-time choice in meta-cmf so a lab built from scratch starts its pods on C | done (29 Sep): the reference workload (emosa-lab `deploy/opensync-lab`, 900 s under six faults, three pods) passed every check with every agent on Python, on C, and mixed, with the same client outages (emosa-lab `doc/evidence/opensync-lab-proof`, fed3224). The RDK room suite on `rdk-emosa-0929` with both pods on C and with one of each gave the Python results: every stage passed, the catalog 27 of 27 and geometry 4 of 4, the rooms that failed on rev120's timing (none on a pod) passing from rev150 (emosa-lab `rdk-lab.md` §9, e89631b). Each run records which implementation each pod ran. The build-time choice: meta-cmf `EASYMESH_EMOSA_AGENT=python\|c` (cc52c79). Both labs are back on Python |

### Phase 5: ready to carry EMOSA in the gateway

Design and evidence only; carrying it starts after this.

| Step | Done when | Status |
| --- | --- | --- |
| 5.1 1905 on the router | EMOSA's virtual agents (their own AL MACs) next to the gateway's own 1905 daemon and agent on `brlan0`: decided | |
| 5.2 The GTP role | the router serves the pods' onboarding and ends their GRE, or supports only the Wi-Fi backhaul and Ethernet pods: decided | |
| 5.3 How pods find EMOSA | the fleet's front port and the redirect on the router's LAN: decided | |
| 5.4 Footprint | the C EMOSA's memory and CPU measured against the gateway container's limit (1 GiB, already tight) | |
| 5.5 Recipe design | an opt-in feature of the layer, off by default: the default image unchanged | |
| 5.6 Code policy | the C implementation is a lab prototype; the path to production code (the board's rule on AI-written code) decided | decided (29 Sep): for this development phase the AI takes the C EMOSA to production quality (CERT C), so it can be evaluated in full; a separate team may take the code on later, without access to these labs, and will own all of it (C, Python reference, spec, vectors). Phase 8 |

**Gate to start carrying EMOSA in the gateway:** phases 1, 3 and 4 done, phase
2 done or deferred on purpose, and the decisions of phase 5 made.

### Phase 6: the RF medium as one component (easymesh-medium)

Today the medium exists twice: meta-cmf-bananapi-vcpe (`gen/wmediumd`,
`gen/hwsim`) and prplmesh-lab (`patches/wmediumd`, `patches/hwsim`,
`wmediumd/`), changed independently (29 Sep: 33 and 8 commits since 20 Sep).
What differs (measured 29 Sep):
- wmediumd: both at upstream `717e5d7`; 32 of the patches are the same under
  other numbers. The patched sources differ in one feature only (prpl's
  "resolve learned VIF identities on readback"); the two success-ACK fixes are
  the same code under two names.
- hwsim: the 11 patches are identical.
- configurator (wmdcfg): 143 files the same, 50 differ (9 code files, chiefly
  the inventory, the observers and the compiler; the tests; 30 goldens), 60
  only in the RDK copy (the pod rooms, the world renderer); none only in prpl.
- observer and console: 48 the same, 9 differ (the per-stack packaging); a
  7.8 MB console binary is checked in on both sides.

| Step | Done when | Status |
| --- | --- | --- |
| 6.1 The repository | `boardfarmdevs/easymesh-medium` holds wmediumd (the upstream pin and one patch series: RDK's plus the one prpl feature), hwsim (its patches, build, cfg80211 notes), the configurator (the world format, the compiler, the rooms), the observer and console (built, not checked in), their tests and a CI that builds and tests all of it without a lab | done (29 Sep): `boardfarmdevs/easymesh-medium`, CI green (wmediumd built and self-tested, configurator tests and golden checks, console tests and build); one hwsim build for both labs (135cb53) |
| 6.2 One configurator | one wmdcfg with the stack-specific parts (inventory: which room role is which lab container and radio) behind a per-stack adapter; one set of rooms per world tree (standard, wired, pods), the goldens regenerated and each difference between the two copies decided and recorded | done locally (29 Sep): `wmdcfg/stacks.py` names the labs' differences; inventory and observers per stack; prplmesh-lab's kernel-medium aliases and stricter apply; RDK's suite plus prplmesh-lab's own tests (233 passed); the three room trees regenerate RDK's goldens identically, so the prplMesh lab gets RDK's rooms (one fix it lacked) |
| 6.3 The labs consume it | meta-cmf-bananapi-vcpe and prplmesh-lab build the medium from a pinned easymesh-medium commit (the workspace sibling, the pin recorded in each lab repo and checked by the build); their own copies are removed; the room builder's parity reference becomes easymesh-medium | done (30 Sep): meta-cmf-bananapi-vcpe (`ee825c5`) and prplmesh-lab (`a2445bc`) consume easymesh-medium as a submodule at `3beae29` (`gen/medium`, `medium`), their own copies removed; the branches `medium-split` merged into `main`. The pin moved from the requalified `036cd3f` by documentation and CI only |
| 6.4 Requalified from scratch | new RDK and prplMesh lab VMs built with the medium from easymesh-medium pass their full suites (as 1.6 and 2.3), and the RDK lab with the EMOSA option passes its suite with the pods (as 3.5) | done (30 Sep): `rdk-0930`, `prpl-0930` and `rdk-emosa-0930` built from scratch on the medium (`036cd3f`), each passed its full suite. `rdk-0930`: 8 of 9 stages on rev140, the one catalog miss (`traffic-low-high-off`, timing) from rev150. `rdk-emosa-0930`: 7 of 9 on rev120, `fifty-client-counter-roam` and the geometry rooms (native stickiness in `backhaul-parent-handover`) from rev150. `prpl-0930`: acceptance with six devices and the optimizer check, the catalog 18 of 27 on rev140 and the other 9 from rev150 (browser timeouts on the loaded host), geometry 4 of 4, static, WebUI and browser 66 of 66. On the way: prplmesh-lab builds the Console on the host (the medium commits no binaries) and forces a restart that times out |
| 6.5 The optimizer | one optimizer for both labs in its own repository, the stacks' differences behind per-stack adapters, pinned by both labs at the same path; requalified in both labs without a rebuild | done (30 Sep): [easymesh-optimizer](https://github.com/boardfarmdevs/easymesh-optimizer) from RDK's `gen/optimizer` history with prplMesh's adapter merged in (`optimizer/stacks.py` names the differences; the prplMesh provider keeps its one-band rounds; the traffic target is the lab's bindings'; prplMesh's load-aware policy is its own file), its manuals moved from the RDK lab, a CI that tests it next to the medium; both labs pin it (`gen/optimizer`, `optimizer`; meta-cmf-bananapi-vcpe `83b4f7a`, prplmesh-lab `551ac95`, optimizer `876d2fb`, medium `19f95d2`; the VMs then moved to the current-state commits `ad840e6` and `7bffef7`). A new `build.sh update` in both labs moves an accepted VM to a commit in place and refuses one that changes what a build installs. The quick requalification (about an hour, instead of rebuilds and full suites): the offline suites (optimizer 504, RDK 1871, prplMesh 2084 passed); `rdk-0930` and `prpl-0930` updated in place, their default rooms settled with the optimizer converged on 20 clients; prplMesh's `optimizer-dynamic.sh recommend` through the merged CLI passed; RDK's CLI, three live `recommend` cycles (20 clients, 340 candidate measurements each); default readiness and five optimizer rooms per lab from rev150 (one-client handover, band upgrade 2.4 to 5, same-band roam, large-room counter-roam, quieter AP), all passed; `rdk-emosa-0930` (rev120) updated in place too, its readiness and two rooms with the pods (one-client handover, large-room counter-roam) passed. RDK's first readiness right after the restart missed its absolute-best criterion by one client 2 RCPI short and passed when rerun. Not run: `build.sh check` (its star topology fits a freshly built VM, not one whose room formed its tree) and RDK's `optimizer-dynamic.sh` (it wants five mesh nodes; the lab has six since the wired extender) |
| 6.6 The room service | the room service (`room_demo`, the live room on port 8891) joins the optimizer in easymesh-optimizer as its second package, with the same per-stack adapters; the viewer stays in easymesh-medium | done (30 Sep): RDK's `room_demo` with its history and prplMesh's copy merged in easymesh-optimizer (`7bfa040`); what the stacks do differently is named in `room_demo/lab.py` (the observer, candidates and topology projection per stack, candidate round size and refresh, verifications in flight, native steering, client names and labels, the wired-AP radio rule, the RDK-only backhaul controls, the CLI's defaults); prplMesh takes RDK's newer room code (profiling, the pods and wired counting, the passive scan before a client joins) and keeps its own settings. The labs keep their launcher, room manifests and bindings and the tests of their own rooms (meta-cmf-bananapi-vcpe `21a132e`, prplmesh-lab `9c9f411`). Offline: 1018 in easymesh-optimizer, RDK 1913, prplMesh 2199. Requalified in place (`build.sh update`): `rdk-0930` and `prpl-0930` readiness, the five optimizer rooms and `backhaul-wired-parent` passed (prplMesh's geometry room on a rerun: the test's own link audit met a client mid-change once); `rdk-emosa-0930` readiness and two rooms with the pods passed. Then renamed `room_service` (easymesh-optimizer `db82faf`, pinned at `c8fbd89` with the medium `0920a19`: meta-cmf-bananapi-vcpe `098968c`, prplmesh-lab `6868c86`); the launcher, the units and their `/run` paths keep `room-demo` until the next VM build. Requalified in place: readiness and the one-client handover room on all three VMs, `backhaul-wired-parent` again on prplMesh. On the way `prpl-0930`'s controller had dropped its wired Agent (`prpl-agent-05`) from its model while the Agent kept answering it (between 19:42 and 19:57, after two runs of `backhaul-wired-parent`); the room service then refused to start (its preflight counts every node). Re-running the Agent's own setup restored it; it stayed in the model through a third run and the 20 minutes after (the cause not found). `radio-lab.sh start-agent`, `stop-agent` and `restart-agent` refused the wired Agent; they take it now and restart each Agent on its own backhaul (prplmesh-lab `6104e4d`, restart-agent 5 on `prpl-0930`). prplMesh's `build.sh update` now brings every pool client online before the room starts, as the RDK lab's does (`fbc8f0c`): twice the room had met clients not yet back and systemd gave up, and one client sat in its SAE 4-way handshake until its cached PMKSA was flushed |
| 6.7 The shared test tooling | the tests and tools both labs carried live with the code they test: the room viewer's and the console's tests in easymesh-medium, the room and optimizer acceptance tools in easymesh-optimizer; the labs' suites run them from there | done (30 Sep): 108 files shared a name in the two labs' test directories, 70 byte-identical. easymesh-medium `configurator/tests/viewer` and `observer/tests` (29 tests, CI runs the 23 without a browser; `61eb51e`); easymesh-optimizer `acceptance/` (the catalog, geometry, readiness, RF, load, counter and traffic tools and their tests, CI runs them; `ec5da31`, `da9f5b2`): the same files taken as they were, the differing ones merged on RDK's newer copy with prplMesh's additions (local host runs, one-step guest installs, its native backhaul probe, `--fail-fast`, the cycle check asserted on prplMesh); one default-room pattern for every room set. Left in the labs: their dashboards', suites', units' and manifests' tests, the render latency tools, `room-world-switch-smoke.py` (written apart per stack). With it: the room service waits up to 120 s for clients and nodes still coming back; `em-optimizer --expected-devices` (the labs have six mesh devices, the policies say five), RDK's `optimizer-dynamic.sh` binds five APs without the wired extender and pods; prplMesh's `build.sh check` documented as a build-time acceptance; both labs' `update` guards leave the medium's tests and docs out; two leftovers of the medium split fixed in RDK (the RF contract step's room test paths, `fullscreen-control-test.js`); the labs block links easymesh-optimizer in all eight repositories. Labs at meta-cmf-bananapi-vcpe `64918a7`, prplmesh-lab `d41ab1e` (optimizer `b0d6780`, medium `e39e98e`). Requalified in place: the offline suites (RDK 1932, prplMesh 2236 with the acceptance tests; the node tests), readiness, the one-client handover room and `backhaul-wired-parent` from `acceptance/` on `rdk-0930` and `prpl-0930`, readiness and a room with the pods on `rdk-emosa-0930`, the medium's six browser tests from their new place. Then open: `prpl-0930`'s controller dropped its wired Agent from its model again within two minutes after `backhaul-wired-parent` returned (its recovery sample at 22:07 had six nodes, 22:08 five); two of four runs today. `radio-lab.sh restart-agent 5` recovers it. Cause (reproduced at 22:32 and 23:07 with the controller's logs): after `prpl-agent-03` roams off the wired Agent's backhaul BSS back to `prpl-agent-01`, it ages `prpl-agent-05` out of its 1905 neighbors (63 s without a discovery message), its next topology response no longer lists it, and prplMesh's `handle_dead_neighbors()` removes a missing wired neighbor whoever reports it (upstream master too); the Agent's own reports then only meet "not found in database". prplmesh-lab patch 0033 removes a wired neighbor only on the report of its inferred wired parent (a compiled test, the unpatched function its negative control; `fb81551`, `abd4ddd`); it takes effect with the next prpl VM build, and `build.sh update` now refuses changed native patches. The geometry harness had passed that run three seconds before the drop: its recovery now holds until the extenders are back on their start parents and 90 s more, at most 150 s (easymesh-optimizer `323e331`, `5e57337`; meta-cmf-bananapi-vcpe `0e99665`, `3afd34a`, `badc808`). Its first live runs: `rdk-0930` passed; on `prpl-0930` one run stopped at the known initial client audit flake, the next caught the drop (recovery at 23:07:13, one node missing from 23:07:42), and `restart-agent 5` recovered it |
| 6.8 Rebuilt from scratch after the splits | every lab VM built again from `main` with the medium, the optimizer and the shared tooling in their own repositories, and its full suite passed | done (1 Oct): `rdk-1001` and `prpl-1001` on rev140 and `rdk-emosa-1001` on rev120 from fresh clones (meta-cmf-bananapi-vcpe `badc808`, prplmesh-lab `abd4ddd`, the medium `e39e98e`, the optimizer `5e57337`, emosa-lab `f947bf3`); the 0930 VMs stopped and kept. Builds: prplMesh artifacts with patch 0033 in 9 min (it compiles with `-Werror`) and the VM in 49; `rdk-1001` 71 min; `rdk-emosa-1001` 53 min plus 11 for the EMOSA option; the RDK images of 29 Sep match `main` (0232 is controller-only), and `rdk-1001` now runs the 0232 controller image too. Suites: `rdk-1001` static 39 of 39 and rooms 9 of 9 (geometry with the browser on rev150: on rev140 one client was still to be steered when the 60 s default recovery ended); `rdk-emosa-1001` rooms 9 of 9 with the pods (`fifty-client-counter-roam` from rev150); `prpl-1001` acceptance and optimizer check, static/WebUI/browser 67 of 67, geometry 4 of 4 with the recovery hold through 150 s and no node lost, the catalog 18 of 27 on rev140 and the other nine from rev150. The EMOSA proof lab `emosa-osl-0925` (rev150) re-staged at `f947bf3`: its 900 s reference workload passed (six faults, all recovered). Found on the way: emosa-lab's adapter kit no longer built its C agent (the fuzz targets needed sources the kit leaves out) and `lab.sh stage` looked for uv only in the opensync-lab cache (`f947bf3`, with a CI step that builds the agent from a kit); `rdk-1001`'s build traffic check lost packets (19, then 3 of 100 clients) while `prpl-1001` ran on the same host and passed with it alone, so rev140 builds and tests one lab at a time |

### Phase 7: documentation that matches the project

About 58 000 lines in 312 documents across the six repositories, with stale
facts (VMs deleted, gaps closed) and documents that mix a current design with
a dated diary. Every document becomes one kind: reference (normative, always
current), guide (how to build and run, always current), plan (carries status),
record (dated evidence, never edited), proposal. Status lives in this plan and
each project's state section; VM and host names in `lab-configurations.md` and
records only.

| Step | Done when | Status |
| --- | --- | --- |
| 7.1 The umbrella | the README and site say what the project is and how to consume it: the goals (optimizer development on RDK and prpl, EMOSA, the physical lab), the two core components, and the rest as infrastructure and learning; current state and building guide current | done (30 Sep, d3a2fa4): the README and the site say what the project is for, the two core components, the infrastructure and learning around them, and where to start; the current state is today's; the labs block shared by the six repositories changes with 7.4 |
| 7.2 emosa-lab | a docs map; the spec, design and C README current (the C agent's state, the target system: `doc/architecture/target-system.md`); `rdk-lab.md` split into its design and its records | done (30 Sep, emosa-lab `6bb3fae`): the docs map by kind; the spec, design and C README match the code and the 5.6 decision; `rdk-lab.md` is the option's design and how to run it, the history moved unchanged into the record `doc/evidence/rdk-lab/README.md` |
| 7.3 The medium and the labs | mostly done (30 Sep): both labs' docs send RF and medium questions to easymesh-medium and keep their own (meta-cmf's radio docs removed, prplmesh-lab's copy of the RF assessment removed, its radio index split into the medium's and the lab's); the medium's docs name its own paths; both labs' current-state pages current. Left: the medium's RF coverage page still carries RDK qualification records, to move to the labs |
| 7.4 opensync-lab, easymesh-lab | the labs block and their state current | done (30 Sep): the labs block (the goals, the two core components) the same in all seven repositories but for the Site line; opensync-lab's status named as the 23 Sep reproduction; easymesh-lab's second extender in the configurations |
| 7.5 Kept current | partly (30 Sep): `pages/check-docs.py`, the same in every repository, checks the labs block and every relative link in each repository's CI (the Pages workflow; easymesh-medium's checks); all pass. Not yet: dated VM names only in records (about 40 outside them, part of them legitimately in plans and proposals) |

### Phase 8: EMOSA C to production quality

The C agent becomes production code (5.6), grown from a basic adapter feature
by feature, each step production quality and gated in the labs. Target: the
RDK lab's containers (bpibroadband, extenders, pods, virtual radios, wmediumd),
now and long term; physical BPI or mv3 routers later. The process model stays
as qualified (a fleet and one agent process per pod); one process for all pods
is a memory optimization for later (9.7), kept possible by holding all of an
agent's state in its context.

| Step | Done when | Status |
| --- | --- | --- |
| 8.1 The bar | written in emosa-lab: CERT C, warnings as errors on gcc and clang, sanitizer-clean tests, fuzzing of every parser of untrusted input, static analysis, a coverage target; the spec, schemas and vectors are the contract; the Python reference stays the vectors' oracle | | written (30 Sep, emosa-lab `c/QUALITY.md`): the contract, CERT C with the project's rules, the gates. Met: warnings as errors on gcc and clang, the tests clean under ASan, LSan and UBSan, the clang analyzer and clang-tidy's CERT checks without findings (from 247; the defects they led to fixed). Partly: fuzzing (four parsers). Not yet: the CERT rules no tool checks, the coverage target (66 % by vectors and units, before the box) |
| 8.2 CI and a lab in a box | emosa-lab's CI builds and tests the C (vectors, units, sanitizers); a harness runs the real binary in a network namespace with a fake pod (an OVSDB server from recorded rows that answers writes), a scripted controller (the reference's wire code) and a broker; every behaviour the rooms rely on and every suite finding is a scenario | | under way: emosa-lab CI builds and tests the C (jobs `c` on gcc, clang and the sanitizers, `c-analyzer`, `c-cert`, `c-fuzz` with four targets); the lab in a box (`emosa_lab.box`, job `ovsdb`) runs either agent against the recorded pod in a real ovsdb-server and a scripted controller: boot, onboard (a real M2 from hostap's registrar, applied and observed) and refuse, both agents alike. Its first finding: the C admitted controllers the reference refuses (fixed, specified and vectored) |
| 8.3 The basic adapter | the fleet and the GTP in C (no Python on a router), and the agent's core: onboarding and renewals, the AP scope, topology and capability reports, the mandatory control answers, the journal and secrets (a secret-store interface: files now, the platform's secure storage later); gated by the harness and by onboarding and client traffic in both labs | |
| 8.4 Feature by feature | telemetry and metrics; client steering; the probe watch; the Multi-AP uplink and Backhaul Steering; each production quality and gated like 8.3 | |
| 8.5 Packaging | the Yocto recipe as an opt-in feature, off by default (5.5); service units; logging through RDK's logger; version, licenses and a bill of materials | |
| 8.6 Evidence and handover | the reference workload and the RDK room suite with the pods on C, and the footprint in the gateway container (5.4), recorded; the handover documents: architecture, module guide, coding standard, test guide, decision log, spec-to-test traceability | |

### Phase 9: EMOSA as a full OpenSync-supporting EasyMesh system

What the design still needs to serve unchanged pods without the OpenSync cloud
(`doc/architecture/target-system.md` in emosa-lab); each item is specified,
vectored, built in the reference and in C, and gated in the labs.

| Step | Done when | Status |
| --- | --- | --- |
| 9.1 Trust without the cloud | TLS on the OVSDB ports and a trust anchor an unchanged pod accepts (with 5.3) | |
| 9.2 Every radio | 5 and 6 GHz fronthaul, several radios per agent, WPA3 | |
| 9.3 Channel and power | the controller's channel and power decisions applied, not declined | |
| 9.4 Ethernet pods | a pod with an Ethernet uplink qualified: transparent, no loop with the GTP, reported truthfully | |
| 9.5 Backhaul | backhaul link metrics and a 1905 neighbor on the backhaul; pods as parents of other pods | |
| 9.6 The router side | EMOSA next to the gateway's own 1905 stack (5.1), the GTP role (5.2), how pods find EMOSA (5.3) | |
| 9.7 Memory | one adapter process for every pod's agent, if the router's memory needs it | |

## Hosts

| Host | In this plan |
| --- | --- |
| rev140 | Yocto builds; the fresh RDK optimizer lab (phase 1.6) |
| rev120 | `rdk-emosa-0929` (phase 3.5; `rdk-emosa` stopped as its backup) and the physical protocol lab; the room tests' browser runs on rev150 |
| rev150 or rev140 | the fresh prplMesh lab (phase 2.3); never rev120 |
