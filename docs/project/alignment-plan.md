# Alignment plan: towards EMOSA in the router

Agreed 2026-09-28. The plan aligned the labs and took EMOSA (in C) to the point where
the RDK gateway image (`bpibroadband`) carries it as an option. Phases 0 to 8 are done, and
EMOSA on the physical mv3 passed its soak with the physical pods (phase 10, 9 October); what
remains is phase 9's last items, the pods over Wi-Fi on the mv3 (10.6) and hardening before a
field trial (phase 11).

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
| 9.5 Backhaul | backhaul link metrics and a 1905 neighbor on the backhaul; pods as parents of other pods | started (8 Oct, layer A on the owner's word; the GRE parent role and prplMesh not approved). Steps 1 and 2 done (emosa-lab c73c105, both agents, spec 8.5): a pod's backhaul station on another pod's backhaul BSS as a 4-address Multi-AP station, no new pod-side writes; each agent reads the fleet's other agents from their statuses; the child names the parent's agent as its 1905 neighbor on the backhaul, the parent names the child on its BSS, and a Link Metric Query for the pair is answered from the parent's measurement of the child's station; a move that would loop the home bridge is refused; a conformance vector, and the box's two-pod scenarios with both agents. RDK's controller takes a BSS for a backhaul candidate only from its own vendor TLV: unified-wifi-mesh 0246 (gateway image 17) takes the role from the BSS Configuration Report, which covers Profile-3 agents but not the RDK lab's pods (EMOSA `r1`, Profile 1, where the controller refuses that report); a fix from the controller's own backhaul SSID is proposed. The owner's step 3 ruling (8 Oct): the future-proof fixes. Step 3 done: unified-wifi-mesh 0247 (the role from the controller's own network SSID), 0248 (a learned station row by its mode and MAC), 0249 (SteerWiFiBackhaul's operating class on every band), 0250 (a Backhaul Steering Response for another station) in gateway image 18; opensync-lab c872deb (the pod bootstrap: a station on every band, the unused ones disabled); emosa-lab 28dfa23 (both agents: a move to another band with that band's station, refusal 0x04, the response naming the station in use, a capability TLV per radio). Steps 4 and 5 done: easymesh-medium 04b64a0 (the inventory's stations per band) and 4c03d11 (the pod room `backhaul-pod-chain`); easymesh-optimizer 33080c8 (a pod's parent: a native AP in reach, else the pod with the best path, on 2.4 GHz) and c070937 (the geometry harness runs the chain room); emosa-lab a6ee41e (`lab.sh move` to a pod). Open: step 6, gateway image 19 (EMOSA 81a93e6) and the new pods on `rdk-1004`, the chain room and the standard pod rooms |
| 9.6 The router side | EMOSA next to the gateway's own 1905 stack (5.1), the GTP role (5.2), how pods find EMOSA (5.3) | started (4 Oct): the gateway image runs EMOSA (lab build option `EASYMESH_EMOSA_IN=gateway`) with its configuration and state on `/nvram/emosa`, which an image upgrade keeps, and the agents' status in RAM; after an upgrade the pods were back within 39 s with the same identities. An agent without a Topology Query for `topology_query_window` (RDK lab: 120 s) onboards again, so the pods come back after a controller restart; the fleet starts its registry's agents itself at boot. Since 6 Oct the fleet, agents and GTP run wholly in the gateway of `rdk-1004`, no containers. Open: a broker and configuration through RDK's data model; TLS is 9.1 |
| 9.7 Memory | one adapter process for every pod's agent, if the router's memory needs it | |

9.2, 9.3 and 9.7 come later, after phase 11. 9.5's layer A started on 8 Oct on the owner's word.

### Phase 10: EMOSA on the physical mv3, passed with the pods (9 October)

The opt-in EMOSA of the gateway image (plan 8.5, meta-cmf's recipe `emosa`) on a physical
mv3, its own RDK EasyMesh next to it, and the physical pods onboarded through it.

Its main work starts when all of these hold (agreed 7 Oct; 5 and 6 are for the soak to
count and do not hold back the porting):

1. Wired pods under EMOSA (9.A1).
2. Extra pods in the fleet's configuration, the Pis' keeper retired (9.A2).
3. The room suite passed with both physical pods present, and the pods' qualification run (9.A3).
4. EMOSA C built and tested 32-bit and with the router's own toolchain: done (10.1).
5. The router has a safe way back to the operator's image: done (7 Oct, verified on the bench).
6. The router's open radio-stack crash is traced or bounded, so that it cannot spoil a soak: bounded (8 Oct): no recurrence in about 11.5 hours under the memory-checking build with three extenders.
7. A design for EMOSA's agents and the pods' VLAN on the router's LAN bridge, beside the
   router's own 1905 instances and its start-up bridging: the main risk. Done (8 Oct):
   EMOSA's agents in a network namespace of their own, joined to the LAN bridge through
   one veth port that the router's start-up leaves alone and a keeper re-adds after the
   operator's LAN rebuilds the bridge; the pods untagged on their VLAN into a LAN port.
8. The interface between the router and the pods agreed: the address the pods dial for
   EMOSA, and where the router keeps EMOSA's configuration and profiles. Done (8 Oct): the
   fleet's front port on the router's LAN address; configuration and state in
   `/nvram/emosa`, as in the RDK image; accepted for the pods (opensync-rpi).
9. The pods' VLAN onto the router's LAN: through a lab host already on both LANs (no new cable), after the pods' soak in the RDK lab: done (8 Oct, 16:24Z).

| Step | Done when | Status |
| --- | --- | --- |
| 10.1 EMOSA C on 32-bit ARM | the C built and its tests passed with the mv3's toolchain (32-bit ARM) | done (7 Oct): built with the mv3's Yocto toolchain (OE 4.0, gcc 11.5, Cortex-A9, soft-float ABI) against the image's own cJSON, OpenSSL 3 and SQLite, the strict warning set with no warning; every test passed under `qemu-arm` with those libraries; no code change needed (emosa-lab `c/QUALITY.md`) |
| 10.2 The recipe in the mv3's image | the `emosa` recipe carried into the mv3's layer, its footprint measured on the board | done (8 Oct): the recipe carried, an image with EMOSA built and flashed; about 7 MB per pod's agent measured on the board |
| 10.3 EMOSA next to the mv3's EasyMesh | its agents beside the router's own 1905 stack on its LAN bridge (5.1), the GTP (5.2) and the redirect (5.3) on the router | prepared off the board (8 Oct): an init script for the router's busybox init, inert until EMOSA's configuration exists, supervising the forwarder and the fleet (restarted 3 s after an exit, as the units do); a keeper that puts the agents' port back into the LAN bridge after the operator's LAN rebuilds it, keeps the fleet's ports open on the LAN and caps EMOSA's logs; a `configure` step from the router's own LAN address and controller; a narrow systemctl stand-in for the fleet's agent commands until emosa-lab's init-agnostic start; checked under emulation; an image with it built, not flashed; the test plans for 10.3 and 10.5 written. The router's kernel lacked network namespaces, which EMOSA's agents use (else the controller takes them for its co-located agent): enabled in the router's EasyMesh images by a kernel configuration fragment, the operator's image unchanged, found off the board, and listed among the BSP patches for the independent review. RDK's controller fix for the crash at a new agent's first onboarding (the copied model's radio count initialised, the radio array bounded; unified-wifi-mesh 0243, found in the RDK lab) carried into the router's controller. The router image with EMOSA (emosa-lab 4b89eab, A1/A2 tested in the RDK lab), its start-up, the namespace kernel and the controller fixes built and checked off the board; flashed after the router's overnight soak, its board run with the way back to the operator's image as well as the suite. emosa-lab's init-agnostic start (the fleet supervising its agents, without systemd) is in; the router moves to it after its first board run, which uses the tested A1/A2 commit, and the board run is repeated on it. First board run (8 Oct): EMOSA running in the router's image beside its own EasyMesh; a simulated OpenSync pod (emosa-lab's remote pod, from a lab host on the router's LAN) onboarded through the router's fleet to its agent and applied the controller's BSS set; controller issues it surfaced are fixed for the next image. The rest of its test plan on the same image (8 Oct): the router's existing suite with EMOSA present passes as with EMOSA inert (the newer extender model's re-onboarding, fixed for the next image, aside), no restart of the router's own EasyMesh; EMOSA's processes come back within 3 s, and after a full restart or a reboot from their kept configuration; the way back to the operator's image and forward again with the new kernel. Found: the operator's LAN rebuild (a change to the LAN's configuration, not normal operation) takes the router's own access points and links out of the bridge until a reboot; EMOSA's keeper puts its own port back in 6 s. Fixed for the next image: the router's start-up re-checks the bridge every 10 s and puts back what is missing (its access points, EasyMesh links and LAN ports), checked off the board and after a real rebuild on the router. Written, not built, for after 10.4: a 2.4 GHz onboarding access point for the pods' Wi-Fi path, outside the LAN and EasyMesh, with EMOSA's GRE termination point on its segment. Done for the wired pods (8 Oct): EMOSA's agents beside the router's own stack. The GTP and the redirect serve pods on a Wi-Fi backhaul only: in the image, not started; they come with 10.6 |
| 10.4 The physical pods on the mv3 | the Pis onboarded over Ethernet through the mv3 | done (8 Oct): after their soak in the RDK lab the two pods moved over Ethernet through a lab host on both LANs, no new cable; they reached the router's EMOSA and its controller at 16:35Z once the router's LAN gave them a default route, and both were configured through EMOSA by 16:53Z (the router's agent check: the three extenders and both pods, each pod's network on its radio); a client served through a pod. Two bench fixes on the way: a router for the pods in the bench DHCP (matched by the pods' DHCP class, kept across a flash), and the pods' first configuration recovering after their restarts |
| 10.5 The suite and a soak with the pods | the router's suite and a soak passed with the pods; the router's open fixes done before the soak | before it (8 Oct, prepared): the next image's regression (the scan-request fix, the bridge re-alignment, the fleet supervising its agents), then an image adding the pods' Multi-AP role (EMOSA finding 21), once the RDK lab has run it and a pod access point with the Multi-AP role is shown to serve an ordinary client; the pods' Multi-AP role checked in their configuration and access points (the upstream hostapd the pods run advertises it only in an association response to a Multi-AP station, so a scan cannot show it), and a client case on it; then the soak with the pods; the router's open fixes done (the way back and the radio-stack crash, 8 Oct). The next image's regression passed (8 Oct): the newer extender's re-onboarding fix seen working (its unanswered scan requests end after three), the bridge restored after the operator's rebuild, the router's own Wi-Fi interface map, the suite 12/12 with all three extenders, the physical pods through a reflash and the way back to the operator's image without help. Found on the bench: without internet the pods restart OpenSync on any loss of their manager (minutes for their clients); a bench uplink through the flash link's host is applied (NAT, bench-only, off by default; the router reaches the internet from its LAN side only, the pods' internet check works), so the soak can include an agent restart the clients ride out. The image with the pods' Multi-AP role and the fix for an operation left indeterminate (EMOSA findings 21 and 22): the pods' fronthaul set to its Multi-AP role, confirmed in the pods' configuration and access points. The soak with the pods started (8 Oct, 19:40Z, 8 hours, on the image with findings 21 and 22 and the bench uplink): every 30 minutes the router's daemons, restarts, memory, crash dumps, EMOSA's processes and each pod agent's state, the controller's devices and ten client cases (the router, the three extenders, each pod's access point); the pods and a client on a pod's access point every minute; one planned fleet restart the pods should ride out. **Passed (9 Oct, the owner's ruling)**: 16 rounds over 7.5 hours; the pods' cases 32 of 32 and both pods connected to EMOSA in every one-minute sample (394), the client on a pod's access point without loss; the planned fleet restart ridden out in about 5 s without an OpenSync restart; no other event (no reboot, daemon restart or crash); EMOSA's memory flat at 24 MB, the router's available memory falling 2.5 MiB/h with its capped in-memory logs. 155 of 160 cases in all: five one-off measurement misses on the extenders' and the router's 5 GHz (a lost ping series or one unmeasured traffic direction, the client associated, with its lease, carrying traffic), none on a pod. The gate now reads: a case fails if its client cannot associate, get its lease or carry traffic; a lost ping series or an unmeasured direction is recorded, and fails only if it repeats for the same case in consecutive rounds. The extenders' 5 GHz ping losses are followed as an item of their own |
| 10.6 No wired pods | both physical pods onboarded over a Wi-Fi backhaul through EMOSA's GTP on the router, 5 GHz on a second adapter per Pi with 2.4 GHz as the start and fallback (one onboarding network on both bands), the router's 5 GHz coming back by itself after a firmware fault, a suite and an 8-hour soak | started (9 Oct, the owner's decision): designed by the router and Pi sides; the router side checked on the board (room for the onboarding access point on both radios; 1600-byte frames on both, so the GRE path carries full frames). The router image with the pods' Wi-Fi path (9 Oct): the onboarding access points created on both radios at boot, before the Wi-Fi stack starts, one onboarding network on both bands, 5 GHz held to channels 36 to 48; switched on through one reboot with nothing by hand, the controller undisturbed, the GTP passing full 1500-byte frames end to end with a test station; the router's suite passed with it. **Both Pis over Wi-Fi (9 Oct, about 07:10Z)**, on 2.4 GHz with their one adapter: every check passed on each (the station on its pinned access point, the GRE underlay at 1600 bytes, the pod's home network, DNS and internet through it, the agent connected), a client through a pod without loss, full frames through the tunnel unfragmented; no wired pods remain. Next: the way back to the operator's image with the path on, the 5 GHz recovery test, the 8-hour soak on one adapter, then 5 GHz with the second adapter. The router's 2.4 GHz channel, left to its own choice, changed only at boots so far |

### Phase 11: hardening before a field trial

After phase 10: the router's remaining fixes, and 9.1 (trust without the cloud: TLS on the
OVSDB ports and a trust anchor an unchanged pod accepts).

### Later

9.2, 9.3, the rest of 9.5 and 9.7; the production plan's other streams (easymesh-resources); a Wi-Fi
backhaul for the physical pods (a second adapter per Pi).

## Hosts

| Host | In this plan |
| --- | --- |
| rev140 | Yocto builds; the target configuration's RDK lab (EMOSA in the gateway) and the physical pods |
| rev120 | the RDK lab with EMOSA reached through the hosts' gateway; RDK only |
| rev150 | container builds, fuzzing and the room tests' browser runs |

The VMs that run on each host now are in [the lab configurations](../reference/lab-configurations.md).
