# Alignment plan: towards EMOSA in the router

Agreed 2026-09-28. The plan aligned the labs and took EMOSA (in C) to the point where
the RDK gateway image (`bpibroadband`) carries it as an option. Phases 0 to 8 are done;
what remains is closing EMOSA in the virtual lab (phase 9), EMOSA on the physical mv3
(phase 10) and hardening before a field trial (phase 11).

## The projects

| Project | Role |
| --- | --- |
| easymesh-medium | the RF medium: wmediumd, hwsim, the configurator and its rooms, the observer and console; one copy both optimizer labs pin |
| easymesh-optimizer | the optimizer, the room service and the shared acceptance tools; pinned by both optimizer labs |
| emosa-lab | EMOSA: its specification and vectors, the Python reference, the C implementation at production quality, the lab in a box |
| meta-cmf-bananapi-vcpe | the RDK optimizer lab (four Wi-Fi extenders and a wired one), with EMOSA as an option of the lab and of the gateway image |
| prplmesh-lab | the prplMesh optimizer lab, with the same wired extender |
| opensync-lab | OpenSync with the mv3 router: learning, and the source of the OpenSync pod image the EMOSA labs pin |
| easymesh-lab | the physical protocol lab: EasyMesh on certified extenders, learning |

The project rests on two core components: **the RF medium** (wmediumd emulating the
radio medium correctly, for every lab) and **EMOSA** (the full conversion between
OpenSync's OVSDB and EasyMesh). Each has one repository with its own specification and
tests; the labs, the room tooling and the learning projects consume them. EMOSA in an
optimizer lab is a configuration of that lab: the adapter, the pods' gateway (GTP) and
at least two OpenSync pods that host clients in the rooms.

## Phases

Order agreed 7 Oct: phase 9's closing work (EMOSA in the virtual lab closed), then 10,
then 11; the rest of 9 later. Status is kept here as the work goes. The step tables of
phases 0 to 8 as they were worked are in this file's history up to 7 October; the
evidence is in each repository's records.

### Phases 0 to 8: done (28 September to 4 October)

| Phase | Result |
| --- | --- |
| 0 Freeze the reference (29 Sep) | the EMOSA 24-room qualification closed; the redeploy order and room waits in meta-cmf (`gen/lab-redeploy.sh`, `gen/lab-bringup.sh`); every input, the OpenSync pod image among them, pinned in `manifest.json` |
| 1 A wired extender in the RDK lab (29 Sep) | `bpiap-004` on the lab's own wired LAN port (`gen/wired-extender.sh`, build stage `56-wired-extenders.sh`), a backhaul parent for the Wi-Fi extenders (rdk-wifi-hal 0045), the `worlds-wired` rooms, topology checks and rooms about it; a lab built from scratch with it passed the full suite |
| 2 The same for prplMesh (29 Sep) | `prpl-agent-05` as the wired agent, the same rooms and checks; built from scratch and passed |
| 3 EMOSA as an option of the RDK lab (29 Sep) | `build.sh emosa` (or `EASYMESH_EMOSA=1` at build) turns it on: EMOSA, fleet, GTP, two pods, rooms (`worlds-pods`, 31 worlds); EMOSA carries out Backhaul Steering, which RDK's controller now sends (unified-wifi-mesh 0232); the pods' fronthaul stays 2.4 GHz (one radio per agent); built from scratch and passed with the pods |
| 4 Python and C interchangeable (29 Sep) | the C agent does what the Python agent does; every behaviour the rooms rely on and every suite finding has vectors both pass; the reference workload and the RDK room suite gave the same results on Python, C and mixed; `EASYMESH_EMOSA_AGENT=python\|c` |
| 5 Ready to carry EMOSA in the gateway (29 Sep to 4 Oct) | the decisions below |
| 6 The RF medium as one component (29 Sep to 1 Oct) | easymesh-medium and easymesh-optimizer (the optimizer, the room service, the acceptance tools) replaced the labs' diverging copies; the controller's topology page, EMOSA's VM steps (`deploy/lib/emosa-vm.sh`) and the latency tools kept once; the RDK lab pins emosa-lab; one lab at a time on a host; unified-wifi-mesh 0233; every lab rebuilt from scratch and requalified |
| 7 Documentation that matches the project (30 Sep to 2 Oct) | every document one kind (reference, guide, plan, record, proposal) in one layout in every repository; `pages/check-docs.py` in each CI; histories squashed per day (1544 commits to 168); lab VMs mask apt's timers and hold snaps; unified-wifi-mesh 0234; every lab rebuilt and requalified |
| 8 EMOSA C to production quality (30 Sep to 4 Oct) | 8.1 the bar (emosa-lab `c/QUALITY.md`: CERT C, warnings as errors, sanitizers, fuzzing, static analysis, coverage); 8.2 CI and the lab in a box (`spec/box-scenarios.md`); 8.3 the fleet and GTP in C, no Python on a router; 8.4 telemetry, steering, the probe watch, the uplink and Backhaul Steering at the same gates; 8.5 packaging (the opt-in recipe `emosa`, units, RDK's logger, an SPDX bill of materials, Apache-2.0); 8.6 the evidence and the handover documents (emosa-lab `docs/handover`); line coverage 90 % with the box, the CERT review of the rules no tool checks done |

Phase 5's decisions, which phases 9 to 11 build on:

| Step | Decision |
| --- | --- |
| 5.1 1905 on the router | each pod an agent of its own on `brlan0` through the package's veth trunk, next to the gateway's own 1905 stack; nothing changes in RDK's agent (4 Oct) |
| 5.2 The GTP role | the gateway runs the GTP (every OpenSync start returns a pod to its GRE bootstrap); the image's EMOSA opt-in brings `emosa-gtp`, enabled and inert until configured (4 Oct) |
| 5.3 How pods find EMOSA | the operator's cloud redirects each admitted pod once to the gateway's fleet front port, and EMOSA presents operator-issued certificates the unchanged pod trusts; TLS is 9.1 (4 Oct) |
| 5.4 Footprint | in the RDK gateway's container about 5 MiB and 0.46 % of a core per agent once the journal was bounded; the gateway at 506 MiB median of its 1 GiB; the reporting policy written only when one is received (3 to 4 Oct) |
| 5.5 Recipe | an opt-in variable of the image (`EMOSA_ADAPTER = "1"`, the GTP with `EMOSA_GTP = "1"`), the default image unchanged (3 Oct) |
| 5.6 Code policy | the AI takes the C EMOSA to production quality so it can be evaluated in full; a later team may own all of it without these labs (29 Sep) |

### Phase 9: EMOSA as a full OpenSync-supporting EasyMesh system

What the design still needs to serve unchanged pods without the OpenSync cloud
(`doc/architecture/target-system.md` in emosa-lab); each item is specified,
vectored, built in the reference and in C, and gated in the labs.

Its closing work comes first (agreed 7 Oct): EMOSA in the virtual lab closed before the
physical router (phase 10). Two physical pods (opensync-rpi's Raspberry Pis, over
Ethernet) are on `rdk-1004`'s controller since 7 Oct.

| Step | Done when | Status |
| --- | --- | --- |
| 9.A1 Ethernet pods (9.4's core) | EMOSA bridges a wired pod's uplink (`eth1`) into its home bridge, and accepts a radio with fewer BSS slots than RDK's set of five, so a pod with fewer serves clients | coded (8 Oct, emosa-lab, both agents): a multi-BSS radio takes a set beyond its slots in part (spec 3.4: the primary BSS and as many per role as the profile has slots); `uplink.mode ethernet` bridges the pod's `eth1` into `br-home` (spec 8.4); the Pis' profile, one AP, in the package. Box 26 of 26. Open: the lab test with the Pis on the rebuilt `rdk-1004` |
| 9.A2 Extra pods in the fleet's configuration | an input of emosa-lab's `fleet_config` for pods beyond the lab's own, replacing opensync-rpi's keeper, which puts the Pis' entries back after every EMOSA run | coded (8 Oct, emosa-lab): the RDK lab's fleet step merges the VM's `/etc/easymesh-lab/emosa-pods.d` (serial to settings, a file per device) into the fleet configuration, so the Pis' entries survive every EMOSA run. Open: opensync-rpi's keeper retired, after the lab test |
| 9.A3 The room suite with the physical pods, and their qualification | the RDK room suite passed with the Pis on the controller; the pods qualified | started (7 Oct): devices the room does not own are listed in the VM's `/etc/easymesh-lab/foreign-devices` and left out of the room's health, the optimizer's observer and the acceptance (easymesh-medium cb6b5ad, easymesh-optimizer d126906, 36f1a5a); with both Pis present the wired extender's outage room passed 3 of 3, then the catalog was run whole |
| 9.1 Trust without the cloud | TLS on the OVSDB ports and a trust anchor an unchanged pod accepts (with 5.3) | moved to phase 11 (7 Oct) |
| 9.2 Every radio | 5 and 6 GHz fronthaul, several radios per agent, WPA3 | |
| 9.3 Channel and power | the controller's channel and power decisions applied, not declined | |
| 9.4 Ethernet pods | a pod with an Ethernet uplink qualified: transparent, no loop with the GTP, reported truthfully | |
| 9.5 Backhaul | backhaul link metrics and a 1905 neighbor on the backhaul; pods as parents of other pods | |
| 9.6 The router side | EMOSA next to the gateway's own 1905 stack (5.1), the GTP role (5.2), how pods find EMOSA (5.3) | started (4 Oct): the gateway image runs EMOSA (lab build option `EASYMESH_EMOSA_IN=gateway`) with its configuration and state on `/nvram/emosa`, which an image upgrade keeps, and the agents' status in RAM; after an upgrade the pods were back within 39 s with the same identities. An agent without a Topology Query for `topology_query_window` (RDK lab: 120 s) onboards again, so the pods come back after a controller restart; the fleet starts its registry's agents itself at boot. Since 6 Oct the fleet, agents and GTP run wholly in the gateway of `rdk-1004`, no containers. Open: a broker and configuration through RDK's data model; TLS is 9.1 |
| 9.7 Memory | one adapter process for every pod's agent, if the router's memory needs it | |

9.2, 9.3, 9.5 and 9.7 come later, after phase 11.

### Phase 10: EMOSA on the physical mv3

The opt-in EMOSA of the gateway image (plan 8.5, meta-cmf's recipe `emosa`) on a physical
mv3, its own RDK EasyMesh next to it, and the physical pods onboarded through it.

Its main work starts when all of these hold (agreed 7 Oct; 5 and 6 are for the soak to
count and do not hold back the porting):

1. Wired pods under EMOSA (9.A1).
2. Extra pods in the fleet's configuration, the Pis' keeper retired (9.A2).
3. The room suite passed with both physical pods present, and the pods' qualification run (9.A3).
4. EMOSA C built and tested 32-bit and with the router's own toolchain: done (10.1).
5. The router has a safe way back to the operator's image: done (7 Oct, verified on the bench).
6. The router's open radio-stack crash is traced or bounded, so that it cannot spoil a soak.
7. A design for EMOSA's agents and the pods' VLAN on the router's LAN bridge, beside the
   router's own 1905 instances and its start-up bridging: the main risk. Done (8 Oct):
   EMOSA's agents in a network namespace of their own, joined to the LAN bridge through
   one veth port that the router's start-up leaves alone and a keeper re-adds after the
   operator's LAN rebuilds the bridge; the pods untagged on their VLAN into a LAN port.
8. The interface between the router and the pods agreed: the address the pods dial for
   EMOSA, and where the router keeps EMOSA's configuration and profiles. Done (8 Oct): the
   fleet's front port on the router's LAN address; configuration and state in
   `/nvram/emosa`, as in the RDK image; accepted for the pods (opensync-rpi).
9. The pods' VLAN cabled to a router LAN port.

| Step | Done when | Status |
| --- | --- | --- |
| 10.1 EMOSA C on 32-bit ARM | the C built and its tests passed with the mv3's toolchain (32-bit ARM) | done (7 Oct): built with the mv3's Yocto toolchain (OE 4.0, gcc 11.5, Cortex-A9, soft-float ABI) against the image's own cJSON, OpenSSL 3 and SQLite, the strict warning set with no warning; every test passed under `qemu-arm` with those libraries; no code change needed (emosa-lab `c/QUALITY.md`) |
| 10.2 The recipe in the mv3's image | the `emosa` recipe carried into the mv3's layer, its footprint measured on the board | started (8 Oct): the recipe carried with emosa-lab pinned at 4b89eab (moved to the commit A1/A2 pass at); an image with EMOSA builds, 128 KiB more root filesystem and 600 kB installed; it differs from the RDK recipe in three ways: no systemd (the router's init; the agents get a stand-in in 10.3), not the RDK logger, no MQTT broker yet. Not flashed: the footprint on the board comes with 10.3 |
| 10.3 EMOSA next to the mv3's EasyMesh | its agents beside the router's own 1905 stack on its LAN bridge (5.1), the GTP (5.2) and the redirect (5.3) on the router | prepared off the board (8 Oct): an init script for the router's busybox init, inert until EMOSA's configuration exists, supervising the forwarder and the fleet (restarted 3 s after an exit, as the units do); a keeper that puts the agents' port back into the LAN bridge after the operator's LAN rebuilds it, keeps the fleet's ports open on the LAN and caps EMOSA's logs; a `configure` step from the router's own LAN address and controller; a narrow systemctl stand-in for the fleet's agent commands until emosa-lab's init-agnostic start; checked under emulation; an image with it built, not flashed; the test plans for 10.3 and 10.5 written. Waits for the tested A1/A2 commit (held: RDK's controller crashed when a one-BSS pod's agent started, under investigation) and the end of the router's overnight soak |
| 10.4 The physical pods on the mv3 | the Pis onboarded over Ethernet through the mv3 | waits for the cabling (the pods' VLAN onto an mv3 LAN port) |
| 10.5 The suite and a soak with the pods | the router's suite and a soak passed with the pods; the router's open fixes done before the soak | |

### Phase 11: hardening before a field trial

After phase 10: the router's remaining fixes, and 9.1 (trust without the cloud: TLS on the
OVSDB ports and a trust anchor an unchanged pod accepts).

### Later

9.2, 9.3, 9.5 and 9.7; the production plan's other streams (easymesh-resources); a Wi-Fi
backhaul for the physical pods (a second adapter per Pi).

## Hosts

| Host | In this plan |
| --- | --- |
| rev140 | Yocto builds; the target configuration's RDK lab (EMOSA in the gateway) and the physical pods |
| rev120 | the RDK lab with EMOSA reached through the hosts' gateway; RDK only |
| rev150 | container builds, fuzzing and the room tests' browser runs |

The VMs that run on each host now are in [the lab configurations](../reference/lab-configurations.md).
