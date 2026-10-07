# Open work

[Documents](../README.md)

The priorities both optimizer labs carry forward, each with its owner and what shows it
done. The [alignment plan](alignment-plan.md) holds the plan, and each project's
proposals what is proposed but not implemented.

| Owner | Work | Completion evidence |
| --- | --- | --- |
| RDK native metrics | Diagnose busy admission and incomplete candidate responses; never mask with stale cache or default retry storms | Timestamped native request/response trace and affected-room rerun |
| RDK 6-GHz association | Correlate BTM, AP refusals, station association and controller publication | Exact target/BSSID/opclass evidence, verified traffic, failures retained |
| prpl metrics interface | Remove whole-second ambiguity with a native sequence ID or higher-resolution timestamp if available | Freshness regression without artificial stale admission |
| Common RF | Qualify fail-closed behavior, overload/drop classification, explicit receiver eligibility and reception-backed measurements | Standalone conformance tests plus a physical reference comparison |
| Common deployment | Consolidate duplicated platform-neutral room/monitoring code only with independent release reproducibility | Both backend unit/import/room gates |
| Hosts | Investigate cooling, throttling and observer load separately from stack logic | Comparable before/after host telemetry |
| OpenSync pods (emosa-lab, opensync-lab) | Cap each pod's systemd journal: journald's default is 10% of the disk up to 4 GiB, and each pod of `rdk-emosa-1005` held 4.0 GiB a day after its build, 8 GiB of the VM's 21 (measured 6 October, for the lab images of easymesh-remote's distribution) | A pod's journal under the cap after a day of rooms; the lab VM's use about 8 GiB lower |
| RDK lab build (meta-cmf-bananapi-vcpe) | After the build, remove boardfarm's build leftovers: the base images, the untagged intermediate layers and the build cache (3 GB on `rdk-emosa-1005`; nearly 4 GB on `rdk-emosa-1006`, whose images were built twice). Keep `bf-wan` and `bf-dhcp-kea`, the only containers that run, and `bf-ssh` only if it is used | `docker system df` after a build: the images in use, no build cache |
| RDK lab build (meta-cmf-bananapi-vcpe) | Keep one gateway and one extender archive in `easymesh-assets` (four of 6 October's gateway builds were kept, 0.3 GiB) and clear apt's caches (0.4 GiB) | One archive per device in `easymesh-assets` after a build |
| RDK lab rooms (meta-cmf-bananapi-vcpe) | Keep room evidence off the lab VM, or bound it: nine runs held 2.3 GiB on `rdk-emosa-1005` | The VM's evidence directory bounded; the evidence kept elsewhere |
| Hosts | The lab VMs' storage pools are `dir`: every snapshot or copy of a VM is its whole 96 GiB disk (a snapshot of `rdk-emosa-1005` took 97 GB on rev120). A ZFS or btrfs pool for lab VMs makes snapshots and copies copy-on-write | A snapshot of a lab VM costs what changed, not the disk |
| RDK controller memory | The controller grows while the mesh keeps re-forming: 643 MiB after about two hours of continuous backhaul drops (2 October), killed at the gateway's 1 GiB limit, which stays. Idle and through the rooms it is flat for two hours. Find what it keeps at each re-formation | The lab's gateway memory profile flat across a run of forced backhaul drops |
| RDK backhaul under host contention | With the lab VM losing about 30% of its CPU time to other work on its host for hours, the extenders left and rejoined the backhaul of the gateway and of the wired extender every 21 seconds; 45 minutes at 25% did not show it. Find which guard leaves, and bound it | The contention replayed for as long, with no drop or with drops that end |
| RDK controller restart | A controller that restarts on its own comes back with part of the model (41 of 60 BSSes eight minutes after a kill); only the lab's ordered bring-up restores it | The controller killed once in a settled lab, the model complete again without the bring-up |
| opensync-lab tests | The lab has no tests: its guest scripts and local-noc are checked only by building the lab | Offline tests of the guest steps and local-noc in its CI |

Larger appliance/inventory refactors are not prerequisites for operating the
current fixed-pool lab. Start with a demonstrated defect and a bounded test,
not another broad architecture proposal. Keep new work items small, assign an
owner and acceptance gate, and remove them when completed. Historical detailed
plans and measurement narratives remain available through Git history.
