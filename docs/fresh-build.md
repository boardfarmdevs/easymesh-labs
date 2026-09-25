# Fresh build of the four labs

Every lab is built again from this workspace, at the pinned commits, following
each project's own guide. The existing work directories and VMs stay as they are
until the new ones pass; nothing here deletes them. A step that needed a
workaround or a change to a project's guide is fixed in that project and noted
here.

## Hosts

| Host | CPUs / memory / free disk (2026-09-25) | Role |
| --- | --- | --- |
| rev140 | 16 / 62 GB / 2.2 TB | Yocto builds: mv3 image, OpenSync pod image, Banana Pi images. Keeps the RDK lab VM `demo-a` until its replacement passes. The old `emosa-osl-0923` and `opensync-lab-0923` VMs retire after the new OpenSync + EMOSA lab passes. |
| rev150 | 16 / 25 GB / 747 GB | The new OpenSync + EMOSA lab VM, 16 GB or more (the old one at 12 GB ran out of memory with six pods). |
| rev120 | 12 / 62 GB / 551 GB | The prplMesh lab, and later the combined end-goal VM (24 to 32 GB). |

Each host gets the workspace at `~/git/easymesh-labs` (`./sync --pinned`).

## Order

1. **Workspace** on rev140, rev150 and rev120: clone this repository,
   `./sync --pinned`.
2. **OpenSync lab** (opensync-lab README):
   - on rev140, `build-mvx.sh pin && build-mvx.sh build` (mv3 image, from the
     local repo mirror) and `build-pod.sh all` (pod image, with the Multi-AP
     link-state patch);
   - copy both images to rev150;
   - on rev150, `setup-vm.sh all` for a new VM, then `deploy-mvx.sh all` and
     `deploy-mvx.sh mesh`. Acceptance: its own checks pass (router, pods,
     clients, local-noc).
3. **EMOSA** on the same VM (emosa-lab `deploy/opensync-lab/README.md`):
   `lab.sh stage`, `controller`, `emosa`, `fleet`, `admit` for every pod,
   `policy`, `gtp`, `ui`, then `option1` on a pod built with the patched image.
   Acceptance: the 900-second workload passes, and the option 1 switch and its
   re-apply after an OpenSync restart pass.
4. **prplMesh lab** on rev120 (prplmesh-lab `deploy/bare-metal/README.md`), in a
   new VM next to `demo-prpl-*`. Acceptance: its full catalog run.
5. **RDK lab** (meta-cmf-bananapi-vcpe `doc/easymesh/build/README.md`): both
   Banana Pi roles built again on rev140, then a new VM. Acceptance: its full
   catalog run from clean source (the current state is "fresh-VM acceptance
   pending").
6. **Pin** the commits that passed (`./pin`) and record the results here.

## Then: the combined system

One VM on rev120 with the EasyMesh controller and native agents on wmediumd, plus
OpenSync pods whose radios are on the same medium, managed through EMOSA. Its
design starts here once the four labs pass on their own.

## Open before step 3

- prplMesh sent AP-Autoconfiguration Renew every few seconds while one EMOSA
  agent was also given the backhaul BSS; understand it before repeating the
  M2-credential test.
