# Lab configurations

The five projects build six VM lab configurations. Four come from one project
each; two add EMOSA to one of those. The sixth, the physical protocol lab, is
the only one tied to hardware: certified extenders and real clients on one host. Each build script names its VM by
default after the configuration and the date (`MMDD`); the names below are
those defaults and the VMs that exist now.

| # | Configuration (VM name) | Built from | Purpose | Current VM (2026-09-29) |
| --- | --- | --- | --- | --- |
| 1 | **RDK EasyMesh lab** (`rdk-MMDD`) | meta-cmf-bananapi-vcpe: both Banana Pi images built on rev140, then `gen/vm/lxd/build.sh build` | EasyMesh optimizer development on RDK: the gateway and controller (`bpibroadband`), 4 Wi-Fi extenders and 1 wired extender (`bpiap`, `EASYMESH_WIRED_EXTENDERS`), 100 room clients, wmediumd, the interactive room with the `worlds-wired` rooms | `rdk-0929` on rev140 (2026-09-29, from scratch; the wired extender a backhaul parent since `f5ad0b2`); `rdk-0925` is the one before the wired extender |
| 2 | **prplMesh lab** (`prpl-MMDD`) | prplmesh-lab: `deploy/lxd-vm/build-artifacts.sh`, then `deploy/lxd-vm/build.sh build` | The same optimizer lab on native prplMesh | `prpl-0929` on rev140 (2026-09-29, from scratch, with the wired Agent `prpl-agent-05`) |
| 3 | **OpenSync lab** (`opensync-lab-MMDD`) | opensync-lab: the mv3 and pod images built on rev140, then `setup-vm.sh all`, `deploy-mvx.sh all` and `deploy-mvx.sh mesh` | A representative router (mv3), OpenSync pods with virtual radios and clients, local-noc as their cloud | none on its own: it is the base of #4 |
| 4 | **OpenSync + EMOSA, prplMesh controller** (`emosa-osl-MMDD`) | #3, then emosa-lab `deploy/opensync-lab/lab.sh`: `stage`, `controller`, `emosa`, `fleet`, `admit`, `policy`, `gtp`, `option1` | Adapter development against a prplMesh controller: several pods, the 900-second workload, the EasyMesh wireless backhaul (option 1) | `emosa-osl-0925` on rev150 |
| 5 | **RDK lab + EMOSA** (`rdk-emosa-MMDD`) | #1 with the EMOSA option: meta-cmf-bananapi-vcpe `EASYMESH_EMOSA=1 gen/vm/lxd/build.sh build` (or `build.sh emosa` on an accepted VM), which runs emosa-lab `deploy/rdk-lab/lab.sh stage` and `lab.sh up` (EMOSA, fleet, GTP, two pods, telemetry, Wi-Fi backhaul, `rooms pods`); `EMOSA_POD_IMAGE` is the pinned pod image. `lab.sh agent POD python\|c` picks a pod's EMOSA implementation; `lab.sh move POD TARGET` has the controller move a pod's backhaul | OpenSync pods as EasyMesh agents in the full RDK lab, next to its native agents and the wired extender on one medium, in the standard rooms with the pods (`worlds-pods`); the controller can move a pod's backhaul (Backhaul Steering). The closest to the end goal so far | `rdk-emosa-0929` on rev120 (2026-09-29, from scratch with the option on; controller image with unified-wifi-mesh 0232; the full room suite with the pods passed, the browser on rev150: emosa-lab `rdk-lab.md` §9); `rdk-emosa` stopped, kept as snapshot `before-replacement-20260929` |
| 6 | **Physical protocol lab** (`easymesh-lab`) | easymesh-lab: `deploy/lxd-vm/build_vm.py` from a clean host checkout, then the USB handover (the Ethernet adapter to the extender, the enrolled USB Wi-Fi clients) | The EasyMesh protocol on certified hardware: a from-scratch Python controller and teaching panel, a TP-Link RE653BE on USB Ethernet (the primary agent) and a second extender, a TP-Link RE715X, onboarded through it onto a Wi-Fi backhaul (experimental, 29 Sep), phones, tablets and laptops on its 2.4, 5 and 6 GHz BSSes, and managed MT7925U Wi-Fi 7 clients for iperf3 | `easymesh-lab` on rev120 (2026-09-28) |

Guides: meta-cmf-bananapi-vcpe `doc/easymesh/build/README.md` (#1), prplmesh-lab
`deploy/bare-metal/README.md` and `deploy/lxd-vm/README.md` (#2), the opensync-lab
README (#3), emosa-lab `deploy/opensync-lab/README.md` (#4) and emosa-lab
`doc/architecture/rdk-lab.md` (#5), easymesh-lab `deploy/lxd-vm/README.md` (#6).

## Hosts

| Host | Runs |
| --- | --- |
| rev140 | the Yocto builds (mv3, OpenSync pod, Banana Pi images); `rdk-0929` (#1, with the wired extender) and `rdk-0925` (#1 before it); `prpl-0929` (#2). With several labs up, run room browser tests from rev150 |
| rev150 | `emosa-osl-0925` (#4) |
| rev120 | `rdk-emosa-0929` (#5; `rdk-emosa` stopped as its backup) and `easymesh-lab` (#6), whose physical devices (the RE653BE's USB Ethernet adapter, the USB Wi-Fi clients) are attached to rev120: physical tests run there. No prplMesh VMs or builders |

## Rebuilding one from scratch

A configuration is reproducible when a fresh build at the pinned commits gives
what the running VM has. `manifest.json` pins the projects and, since
2026-09-28, the images built outside a lab VM (the OpenSync pod image, the
Banana Pi images) with the commit each was built from. New Banana Pi images go
into a running RDK lab with meta-cmf-bananapi-vcpe `gen/lab-redeploy.sh`.
On 2026-09-29 every configuration above except #3 has a VM built from
scratch at pinned commits: #1 `rdk-0929`, #2 `prpl-0929`, #5 `rdk-emosa-0929`
(one command, the EMOSA option of #1); #5 passed its full suite with the pods,
with the pods' agents on Python, on C and mixed (alignment plan 3.5 and 4.3). On
30 September #1, #2 and #5 are being built again from scratch on
[easymesh-medium](https://github.com/boardfarmdevs/easymesh-medium), the RF medium
both optimizer labs now share (plan 6.4); the table is updated when they pass.

## Not (yet) a configuration

- **The combined end-goal system**: one controller, native agents and OpenSync
  pods on one medium, with the pods in the room model. #5 is that on the RDK
  side, as an option of the RDK lab; EMOSA inside the gateway image is the
  step after [the alignment plan](alignment-plan.md).
- **EMOSA in the prplMesh lab** (#2 with EMOSA): never built.
- **emosa-lab's early qualification setups** (`deploy/create-vm.sh`,
  `deploy/reliability`): their VMs were deleted on 2026-09-24.
