# Lab configurations

The five projects build six VM lab configurations. Four come from one project
each; two add EMOSA to one of those. The sixth, the physical protocol lab, is
the only one tied to hardware: certified extenders and real clients on one host. Each build script names its VM by
default after the configuration and the date (`MMDD`); the names below are
those defaults and the VMs that exist now.

| # | Configuration (VM name) | Built from | Purpose | Current VM (2026-09-28) |
| --- | --- | --- | --- | --- |
| 1 | **RDK EasyMesh lab** (`rdk-MMDD`) | meta-cmf-bananapi-vcpe: both Banana Pi images built on rev140, then `gen/vm/lxd/build.sh build` | EasyMesh optimizer development on RDK: the gateway and controller (`bpibroadband`), 4 Wi-Fi extenders and 1 wired extender (`bpiap`, `EASYMESH_WIRED_EXTENDERS`), 100 room clients, wmediumd, the interactive room with the `worlds-wired` rooms | `rdk-0929` on rev140 (2026-09-29, from scratch); `rdk-0925` is the one before the wired extender |
| 2 | **prplMesh lab** (`prpl-MMDD`) | prplmesh-lab: `deploy/lxd-vm/build-artifacts.sh`, then `deploy/lxd-vm/build.sh build` | The same optimizer lab on native prplMesh | none (`prpl-0925` on rev120 was deleted: rev120 is kept for #5) |
| 3 | **OpenSync lab** (`opensync-lab-MMDD`) | opensync-lab: the mv3 and pod images built on rev140, then `setup-vm.sh all`, `deploy-mvx.sh all` and `deploy-mvx.sh mesh` | A representative router (mv3), OpenSync pods with virtual radios and clients, local-noc as their cloud | none on its own: it is the base of #4 |
| 4 | **OpenSync + EMOSA, prplMesh controller** (`emosa-osl-MMDD`) | #3, then emosa-lab `deploy/opensync-lab/lab.sh`: `stage`, `controller`, `emosa`, `fleet`, `admit`, `policy`, `gtp`, `option1` | Adapter development against a prplMesh controller: several pods, the 900-second workload, the EasyMesh wireless backhaul (option 1) | `emosa-osl-0925` on rev150 |
| 5 | **RDK lab + EMOSA** (`rdk-emosa`) | #1, then emosa-lab `deploy/rdk-lab/lab.sh`: `stage`, `lanport`, `emosa`, `fleet`, `gtp`, `pod pod-1`, `pod pod-2`, `telemetry`, `backhaul wifi`; then meta-cmf-bananapi-vcpe `gen/bpi.sh -i 4` and `gen/wired-extender.sh up 4` (the wired extender); then `lab.sh rooms pods-wired`. `lab.sh agent POD python\|c` picks a pod's EMOSA implementation | OpenSync pods as EasyMesh agents in the full RDK lab, next to its native agents on one medium: two pods on Wi-Fi backhaul (or the GTP path), a wired extender, and the 24-room suite with both in the room model. The closest to the end goal so far | `rdk-emosa` on rev120, on the 239f9f6 images since 2026-09-28 |
| 6 | **Physical protocol lab** (`easymesh-lab`) | easymesh-lab: `deploy/lxd-vm/build_vm.py` from a clean host checkout, then the USB handover (the Ethernet adapter to the extender, the enrolled USB Wi-Fi clients) | The EasyMesh protocol on certified hardware: a from-scratch Python controller and teaching panel, a TP-Link RE653BE on USB Ethernet, phones, tablets and laptops on its 2.4, 5 and 6 GHz BSSes, and managed MT7925U Wi-Fi 7 clients for iperf3 | `easymesh-lab` on rev120 (2026-09-28) |

Guides: meta-cmf-bananapi-vcpe `doc/easymesh/build/README.md` (#1), prplmesh-lab
`deploy/bare-metal/README.md` and `deploy/lxd-vm/README.md` (#2), the opensync-lab
README (#3), emosa-lab `deploy/opensync-lab/README.md` (#4) and emosa-lab
`doc/architecture/rdk-lab.md` (#5), easymesh-lab `deploy/lxd-vm/README.md` (#6).

## Hosts

| Host | Runs |
| --- | --- |
| rev140 | the Yocto builds (mv3, OpenSync pod, Banana Pi images); `rdk-0929` (#1, with the wired extender) and `rdk-0925` (#1 before it); the fresh prplMesh VM (#2, plan 2.3) |
| rev150 | `emosa-osl-0925` (#4) |
| rev120 | `rdk-emosa` (#5) and `easymesh-lab` (#6), whose physical devices (the RE653BE's USB Ethernet adapter, the USB Wi-Fi clients) are attached to rev120: physical tests run there. No prplMesh VMs or builders |

## Rebuilding one from scratch

A configuration is reproducible when a fresh build at the pinned commits gives
what the running VM has. `manifest.json` pins the projects and, since
2026-09-28, the images built outside a lab VM (the OpenSync pod image, the
Banana Pi images) with the commit each was built from. New Banana Pi images go
into a running RDK lab with meta-cmf-bananapi-vcpe `gen/lab-redeploy.sh`.
Open on 2026-09-28, each a step of [the alignment plan](alignment-plan.md):

- **#5 has never been built from scratch.** `rdk-emosa` was made from
  `rdk-0925`'s images on 2026-09-25 and has grown in place since; the stages
  above are the order, not yet one command (plan 3.2, 3.5).
- **The wired extender is not yet a backhaul parent.** RDK's extender mode
  does not act on its Ethernet uplink: its own backhaul BSS stays down and its
  `brlan0` gets no DHCP address (plan 1.2).
- **#2 has no VM.** prplmesh-lab carries the wired Agent since 2026-09-29; a
  fresh VM with it is plan 2.3.

## Not (yet) a configuration

- **The combined end-goal system**: one controller, native agents and OpenSync
  pods on one medium, with the pods in the room model. #5 holds it on the RDK
  side; [the alignment plan](alignment-plan.md) makes it an option of the RDK
  lab.
- **EMOSA in the prplMesh lab** (#2 with EMOSA): never built.
- **emosa-lab's early qualification setups** (`deploy/create-vm.sh`,
  `deploy/reliability`): their VMs were deleted on 2026-09-24.
