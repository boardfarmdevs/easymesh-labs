# Lab configurations

The four projects build five VM lab configurations. Three come from one project
each; two add EMOSA to one of those. Each build script names its VM by
default after the configuration and the date (`MMDD`); the names below are
those defaults and the VMs that exist now.

| # | Configuration (VM name) | Built from | Purpose | Current VM (2026-09-25) |
| --- | --- | --- | --- | --- |
| 1 | **RDK EasyMesh lab** (`rdk-MMDD`) | meta-cmf-bananapi-vcpe: both Banana Pi images built on rev140, then `gen/vm/lxd/build.sh build` | EasyMesh optimizer development on RDK: the gateway and controller (`bpibroadband`), 4 native extenders (`bpiap`), 100 room clients, wmediumd, the interactive room | `rdk-0925`; `demo-a` on rev140 is the older one |
| 2 | **prplMesh lab** (`prpl-MMDD`) | prplmesh-lab: `deploy/lxd-vm/build-artifacts.sh`, then `deploy/lxd-vm/build.sh build` | The same optimizer lab on native prplMesh | none (`prpl-0925` on rev120 was deleted: rev120 is kept for #5) |
| 3 | **OpenSync lab** (`opensync-lab-MMDD`) | opensync-lab: the mv3 and pod images built on rev140, then `setup-vm.sh all`, `deploy-mvx.sh all` and `deploy-mvx.sh mesh` | A representative router (mv3), OpenSync pods with virtual radios and clients, local-noc as their cloud | none on its own: it is the base of #4 |
| 4 | **OpenSync + EMOSA, prplMesh controller** (`emosa-osl-MMDD`) | #3, then emosa-lab `deploy/opensync-lab/lab.sh`: `stage`, `controller`, `emosa`, `fleet`, `admit`, `policy`, `gtp`, `option1` | Adapter development against a prplMesh controller: several pods, the 900-second workload, the EasyMesh wireless backhaul (option 1) | `emosa-osl-0925` on rev150 |
| 5 | **RDK lab + EMOSA** (`rdk-emosa`) | #1, then emosa-lab `deploy/rdk-lab/lab.sh`: `stage`, `lanport`, `emosa`, `fleet`, `gtp`, `pod`, `client`, `agent` | OpenSync pods as EasyMesh agents in the full RDK lab, next to its native agents on one medium; the swap between the Python and the C agent. The closest to the end goal so far | `rdk-emosa` on rev120 |

Guides: meta-cmf-bananapi-vcpe `doc/easymesh/build/README.md` (#1), prplmesh-lab
`deploy/bare-metal/README.md` and `deploy/lxd-vm/README.md` (#2), the opensync-lab
README (#3), emosa-lab `deploy/opensync-lab/README.md` (#4) and emosa-lab
`doc/architecture/rdk-lab.md` (#5).

## Hosts

| Host | Runs |
| --- | --- |
| rev140 | the Yocto builds (mv3, OpenSync pod, Banana Pi images); `demo-a` (#1) until its replacement passes |
| rev150 | `emosa-osl-0925` (#4) |
| rev120 | `rdk-emosa` (#5) only. No prplMesh VMs or builders: the whole host is kept for this lab |

## Rebuilding one from scratch

A configuration is reproducible when a fresh build at the pinned commits gives
what the running VM has. Known gaps on 2026-09-25:

- **Pins behind the work.** `manifest.json` pins emosa-lab, opensync-lab and
  meta-cmf-bananapi-vcpe at commits older than what #4 and #5 run (among
  others the pod's steering fixes, the Python and C agents and em_cli's marking
  of OpenSync pods). `./pin` records the current commits once they are pushed.
- **#5's controller image.** em_cli's marking of OpenSync pods was installed
  into the running `rdk-emosa`, not built into its images. A clean #5 needs
  the Banana Pi images built again at the meta-cmf-bananapi-vcpe commit that
  carries it, and a full acceptance run of the new VM.
- **The pod image.** #4 and #5 run a pod image built from opensync-lab
  (`build-pod.sh`) whose stamp is recorded in the emosa-lab evidence
  (`mvx-pod-20260925075828` for #5), not in the manifest.
- **Staged, not one command.** #4 and #5 are a sequence of stages on top of
  #3 and #1, in the order their guides give.

## Not (yet) a configuration

- **The combined end-goal system**: one controller, native agents and OpenSync
  pods on one medium, with the pods in the room model. #5 already holds most
  of it on the RDK side.
- **EMOSA in the prplMesh lab** (#2 with EMOSA): never built.
- **emosa-lab's early qualification setups** (`deploy/create-vm.sh`,
  `deploy/reliability`): their VMs were deleted on 2026-09-24.
