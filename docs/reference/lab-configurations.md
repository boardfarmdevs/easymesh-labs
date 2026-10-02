# Lab configurations

The projects build six VM lab configurations. Four come from one project each; two add
EMOSA to one of those. The sixth, the physical protocol lab, is the only one tied to
hardware: certified extenders and real clients on one host. Each build script names its
VM by default after the configuration and the date (`MMDD`).

| # | Configuration (VM name) | Built from | Purpose | Current VM |
| --- | --- | --- | --- | --- |
| 1 | **RDK EasyMesh lab** (`rdk-MMDD`) | meta-cmf-bananapi-vcpe: the Banana Pi images, then `gen/vm/lxd/build.sh build` | optimizer development on RDK: the gateway and controller (`bpibroadband`), 4 Wi-Fi extenders and 1 wired extender, 100 room clients, wmediumd, the interactive room | `rdk-1001` on rev140 |
| 2 | **prplMesh lab** (`prpl-MMDD`) | prplmesh-lab: `deploy/lxd-vm/build-artifacts.sh`, then `deploy/lxd-vm/build.sh build` | the same optimizer lab on native prplMesh, with a wired Agent | `prpl-1001` on rev140 |
| 3 | **OpenSync lab** (`opensync-lab-MMDD`) | opensync-lab: the mv3 and pod images, then `setup-vm.sh all`, `deploy-mvx.sh all` and `deploy-mvx.sh mesh` | a representative router (mv3), OpenSync pods with virtual radios and clients, local-noc as their cloud | none on its own: the base of #4 |
| 4 | **OpenSync + EMOSA, prplMesh controller** (`emosa-osl-MMDD`) | #3, then emosa-lab `deploy/opensync-lab/lab.sh` (`stage`, `controller`, `emosa`, `fleet`, `admit`, `policy`, `gtp`, `option1`) | adapter development against a prplMesh controller: several pods, the 900-second fault workload, the EasyMesh wireless backhaul | `emosa-osl-0925` on rev150 |
| 5 | **RDK lab + EMOSA** (`rdk-emosa-MMDD`) | #1 with the EMOSA option: `EASYMESH_EMOSA=1 gen/vm/lxd/build.sh build` (or `build.sh emosa` on an accepted VM), which runs emosa-lab at the commit the RDK lab pins | OpenSync pods as agents next to the RDK lab's native agents, in the standard rooms with the pods | `rdk-emosa-1001` on rev120 |
| 6 | **Physical protocol lab** (`easymesh-lab`) | easymesh-lab: `deploy/lxd-vm/build_vm.py`, then the USB handover (the Ethernet adapter to the extender, the USB Wi-Fi clients) | the EasyMesh protocol on certified hardware: a from-scratch controller and teaching panel, a TP-Link RE653BE and a second extender, real clients | `easymesh-lab` on rev120 |

Each project's site links its build guide: the RDK lab's for #1 and #5, prplmesh-lab's
for #2, opensync-lab's for #3, emosa-lab's for #4 and #5, easymesh-lab's for #6.
`manifest.json` pins the projects and the images built outside a lab VM (the OpenSync pod
image, the Banana Pi images) with the commit each was built from; a fresh build at the
pins gives what the running VMs have.

## Hosts

| Host | Runs |
| --- | --- |
| rev140 | the Yocto builds (mv3, OpenSync pod, Banana Pi images); `rdk-1001` (#1) and `prpl-1001` (#2), one lab building or testing at a time (their builds and checks refuse while the other runs); room browser tests run from rev150 |
| rev150 | `emosa-osl-0925` (#4); the room browser for the labs on rev140 and rev120, container builds and fuzzing |
| rev120 | `rdk-emosa-1001` (#5) and `easymesh-lab` (#6), whose physical devices are attached to rev120: physical tests run there. No prplMesh VMs or builders |

## Reaching a lab

Each lab VM publishes its web interfaces as ports on its host, on the lab network. Which
interfaces each configuration has, and how a lab is reached from outside the lab network
(the gateway, with a login and one reservation), is in
[easymesh-remote](https://vcpe.dev/easymesh-remote/). The gateway serves the RDK lab's
layout (#1 and #5) today.

## Not (yet) a configuration

- **The combined end-goal system**: one controller, native agents and OpenSync pods on
  one medium, with the pods in the room model. #5 is that on the RDK side, as an option
  of the RDK lab; EMOSA inside the gateway image is the step after
  [the alignment plan](../project/alignment-plan.md).
- **EMOSA in the prplMesh lab** (#2 with EMOSA): never built.
