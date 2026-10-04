# Faster, cheaper labs: precooked layers and less rebuilding

[Documents](../README.md)

**Kind:** proposal. **Status:** implemented in both optimizer labs and verified on rev140,
3 and 4 October 2026 ([section 5](#5-status-4-october-2026)); two points open. **Prepared:**
3 October 2026, from measurements of the RDK and prplMesh labs on rev140 (sources in section 1).

The time it takes to build and requalify a lab is the labs' largest running cost: every
change to a shared part means rebuilding both optimizer labs and running their suites. This
proposal says where that time goes today, what is already precooked, and what to change,
ranked by what it saves against what it costs.

## 1. Where the time goes

| Stage | Time | How often its inputs change | Precooked today |
| --- | --- | --- | --- |
| RDK lab: the BPI images (Yocto) | 4 to 13 min on rev140 (the last 11 builds); hours on a host without a warm cache | the manifest, recipes and configuration: 0 to 2 commits in the last 30 days | rev140's sstate cache: over 99 % of the tasks reused (5,766 of 5,792 for the controller). On rev140 only |
| prplMesh lab: the native archives (prplMesh, its dependencies, hostap 2.10) | built in a builder VM; not timed in its records | the build scripts: 1 to 2 commits; the native patches: 15 | three archives (141 MB, built 28 September) reused by every VM build. On rev140 only, not keyed by the inputs they were built from |
| Lab VM build, RDK | about 55 min ([its guide](https://vcpe.dev/meta-cmf-bananapi-vcpe/)): base OS, kernel and nested LXD 6 min; WAN and Boardfarm 9 min; mesh and 100 clients 24 min; runtime 2 min; cold-boot acceptance 12 min; audit 2 min | the VM's scripts: 27 commits in 30 days | nothing: every build starts from a bare Ubuntu image |
| Lab VM build, prplMesh | the same shape; no phase timings recorded | the deploy scripts: 22 commits | nothing beyond the native archives |
| A change applied to an accepted VM | minutes: both labs' `build.sh update` | — | — |
| …unless it touches the medium's daemon, console or radio module, the guest's services, the container scripts or the native patches | a full build | the medium's `wmediumd`: 14 commits in 30 days | `update` refuses and asks for a build |
| Requalification | the room suite (27 rooms, not timed in the records) and a 12-hour soak | every change | — |
| Running | RDK VM: 8 vCPUs, 16 GiB, about 4 GiB used with 106 containers, 12 GB of disk; prplMesh VM: 16 GiB, 160 GiB disk | — | all VMs `boot.autostart=false` |

The commit counts understate the change rate: the lab histories were squashed on
2 October. They still show the pattern that matters: **the slow-to-build parts change
rarely, the fast ones change daily, and a daily change still often costs a full build.**

## 2. What to do

Ranked by saving against cost. The savings are estimates from section 1, to be checked by
the first step.

| # | Change | What it saves | Cost | First step |
| --- | --- | --- | --- | --- |
| 1 | **Time every build and suite** | makes every other item measurable; the RDK guide's 55-minute table was reconstructed by hand | small | each build and suite writes its phase times to its record, as the BPI image builds already do |
| 2 | **Make `update` cover the medium and the guest's services** | most daily changes stop costing a full build: a changed `wmediumd` is rebuilt in the VM (seconds), services reinstalled and restarted | moderate: the update must leave the VM as a build would, and prove it | apply a medium change by `update` and by a build to two copies of one VM, and compare them |
| 3 | **Requalify what a change can affect** | most of a suite run, most of the time | moderate: a written map from component to suites, kept current | the map: medium daemon to RF and rooms; optimizer to rooms; clients to steering and rooms; UI to browser. The full suite and the 12-hour soak at release points only |
| 4 | **A precooked base VM image** | about 12 of the RDK build's 55 min: the OS, the radio kernel, nested LXD and hwsim, and the WAN and Boardfarm setup come in one import, and the nested mesh and client images with it | moderate: an image per lab, rebuilt when its own inputs change | build the RDK image from the stages a build runs before its mesh deployment, keyed by those stages' inputs |
| 5 | **An artifact store keyed by inputs** | hours on any host but rev140: each slow part is built once per input digest and fetched everywhere else | small to moderate | publish the BPI images (keyed by the manifest and the layer's recipes), the prplMesh native archives (keyed by the source revisions and the patch digest) and the base images of item 4; GitHub release assets, as emosa-lab already does for its evidence, or an HTTP store on rev140 |
| 6 | **A shared sstate mirror** | a cold Yocto build on rev120 or rev150 becomes a warm one: minutes instead of hours | small | serve rev140's sstate cache over HTTP and name it in the image helper's `SSTATE_MIRRORS` |
| 7 | **Copy-on-write storage for lab VMs** | a copy or snapshot of an accepted VM in seconds instead of minutes, and a fraction of the disk; experiments run on copies, as the client bench ran on five | small: a Btrfs or ZFS pool; the labs default to `dir` | build one lab on a Btrfs pool and time a copy; the prplMesh lab already uses Btrfs for its nested containers |
| 8 | **One Alpine client image for both labs** | smaller client images and a faster 100-client expansion (the RDK lab's mesh-and-clients phase is 24 min, with its association gates) | moderate: the prplMesh lab's clients are Ubuntu 22.04 | with easymesh-clients' shared build, which builds on any OS; planned separately |
| 9 | **A small development profile** | iteration on a lab with 20 clients instead of 100: less creation time and memory | small | a build option; qualification keeps the lab's full capacity of 100 clients |

## 3. What not to change

- **No binaries in git.** The prplMesh archives are already kept out for size; artifacts go
  to a store with their checksums, as emosa-lab's evidence does.
- **No shortened gates.** The RDK guide's rule stays: the build's acceptance and the suites
  decide when a lab is ready; precooking changes how the lab gets there, not what it must
  pass.
- **Provenance travels with every artifact**: what it was built from (commits, digests,
  options), as the client build's `build.env` and the BPI images' build evidence record
  today.

## 4. Order

Item 1 first, because it measures the rest. Then items 2 and 3, which save the most on the
change that happens every day. Then items 5 and 6, which matter as soon as a second host
builds labs. Then 4 and 7, which make a fresh lab or an experiment cheap. Item 8 follows the
client plan, and item 9 can come at any time.

## 5. Status, 4 October 2026

All nine are in both optimizer labs (meta-cmf-bananapi-vcpe and prplmesh-lab, each lab's
`docs/reference/build-speed.md`) and in this repository (the store's server, `artifacts/`,
and [its reference](../reference/artifact-store.md)). Verified on rev140 with test VMs built
for it, beside another agent's running lab:

| # | Change | Where it is | Verified |
| --- | --- | --- | --- |
| 1 | Times | every build, update and copy writes `build-evidence/KIND-NAME-STAMP/` (`phases.tsv`, `summary.txt`); the suites' `summary.json` carries each section's seconds | every number below comes from those records |
| 2 | `update` covers the medium and the guest | both labs: the medium's daemon, console and radio module, the guest's services (and in prplMesh the controller UI and the containers' scripts) are rebuilt and installed, then the VM restarts; an update stopped part-way is finished by running it again | RDK: a copy updated to a commit changing the daemon, console, radio module and a guest tool in 33 min (5 of building and installing, 28 of restart and bring-up) where a build takes 73 from the base image; its checkout, module and tool checked in the VM, and it passed `check` in full. prplMesh: a copy updated to a commit changing the medium, a guest service and a client script in 18.9 min where a build takes 45.6, then passed `check` in full |
| 3 | Requalify what a change can affect | both labs: `affected-suites.py BASE`, its map kept by unit tests | prints the step and the sections, following the submodules |
| 4 | A base VM image | both labs: the stages that do not depend on the commit, as an LXD image named by their inputs, made and published on the way | RDK: base stages 1293 s cold, 119 s from the image fetched from the store (`rdk-fast-b` then passed its acceptance). prplMesh: 5.5 min saved a build (its base is small); `prpl-fast-a` from its base passed its acceptance in 45.6 min |
| 5 | The artifact store | rev140:8180; the RDK images and base image, the prplMesh native archives, its client supplicant and base image | prplMesh native archives built in 15.5 min and fetched in 4 s; the RDK base image fetched and imported in under 85 s. The RDK images' publish and fetch are not yet exercised live (the cold image build stops, item 6) |
| 6 | The sstate mirror | `BUILD_SSTATE_MIRROR` in the RDK image helper | a cold workspace restored 5,750 of 5,769 tasks from it in under 7 minutes; **open**: one task it ran itself fails (ccsp-one-wifi's packaging, under pseudo), so a cold image build stops there |
| 7 | Copy-on-write copies | both labs: `build.sh copy NEW` on a Btrfs or ZFS pool | a copy of an accepted lab in 8 s (RDK, sharing 9 GiB) and 7 s (prplMesh, 13.9 GiB); each started on its own address and ports |
| 8 | Alpine clients | prplMesh: the clients' supplicant built for musl from the lab's pinned hostap and patches | 100 of 100 Alpine clients associated and reached the controller in `prpl-fast-a`'s acceptance; the client image is 45.7 MB against the 366 MB Ubuntu one |
| 9 | A development lab | both labs: `EASYMESH_DEV_CLIENTS` / `PRPLMESH_DEV_CLIENTS=20`, no room service, never packaged | |

Found on the way and fixed: a base publish restarts the VM, and the RDK build went on before
Boardfarm had rebuilt its WAN; the prplMesh guest held its shutdown past the publish's
timeout; Alpine's first package fetch ran before the builder container had its network.
Found and fixed in `start`: when the runtime's own gate stops on an extender registered
without its BSSes, the bring-up that repairs that now runs before a second start. Seen and
**open**, not from these changes: with three lab VMs on rev140, 25 of a lab's 100 clients
lost packets in `check`'s traffic gate, as 19 did on 1 October.
