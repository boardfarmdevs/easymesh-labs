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
| Lab storage (the labs, the hosts) | A lab VM with pods holds 21 to 35 GB of which about 7 is the lab: the pods' journals at journald's 4 GiB default, unbounded room evidence, boardfarm's Docker build leftovers, superseded archives; every lab VM in a `dir` pool of its own, where a snapshot is the whole disk. Measured on 6 October; eleven work items (a ZFS pool per host, the builds defaulting to it, every log and evidence store bounded) in easymesh-resources, `lab-storage/README.md` (private, not on its site) | Its definition of done: every lab VM in the hosts' `labs` pool, each with pods at 10 GB or less after a day of rooms (`lab-storage/tools/measure.sh`) |
| Lab memory (the labs, the hosts) | A lab VM is given 16 GiB and needs about 6.6, and its host keeps all 16: the VMs' balloon device does not report free pages, so each lab's QEMU holds 14 to 16 GiB whatever the lab uses. LXD's monitor, 20 MiB per running container, is the largest program: 2.1 GiB for 108 containers, 80 of them clients the default room takes off the air but leaves running. Measured on 7 October; nine work items (free page reporting, the guest's cache kept small, only the room's clients running, the VM's limit right-sized to what the heaviest room needs) in easymesh-resources, `lab-memory/README.md` (private), and [its page](https://vcpe.dev/easymesh-resources/lab-memory/) | Its definition of done: each running lab's QEMU following its use (5.5 to 7 GiB for an RDK lab), no OOM kills, the labs' limits at what their heaviest rooms need (`lab-memory/tools/measure.sh`) |
| RDK controller memory | The controller grew to 643 MiB after about two hours of continuous backhaul drops (2 October, an older image, the host under contention), killed at the gateway's 1 GiB limit, which stays. Forced re-formations do not reproduce it on image 12 (8 October, rdk-emosa-1005: 40 extender outages and 120 flaps of all four extenders, em_ctrl flat at 44 to 71 MiB; easymesh-resources lab-memory, measurements of 8 October), but its high-water mark there is 317 MiB from something else. Find what drives that peak (the hundred-client rooms, the catalog) and whether the growth needed the host's contention | The lab's gateway memory profile flat across a run of forced backhaul drops |
| RDK backhaul under host contention | With the lab VM losing about 30% of its CPU time to other work on its host for hours, the extenders left and rejoined the backhaul of the gateway and of the wired extender every 21 seconds; 45 minutes at 25% did not show it. Find which guard leaves, and bound it | The contention replayed for as long, with no drop or with drops that end |
| RDK controller restart | A controller that restarts on its own comes back with part of the model (41 of 60 BSSes eight minutes after a kill); only the lab's ordered bring-up restores it | The controller killed once in a settled lab, the model complete again without the bring-up |
| opensync-lab tests | The lab has no tests: its guest scripts and local-noc are checked only by building the lab | Offline tests of the guest steps and local-noc in its CI |
| RDK patch series checks | Two of the series' compiled source checks fail on the fully patched tree, and did before 0247 (found 8 October): `gen/tests/policy-ack-ownership-test.py` (its model lacks `em_util_dbg_print` from 0237; with it added, a policy ACK also completes another radio's pending policy command, which the check says must not happen) and `gen/tests/native-backhaul-agent-test.py` (`root_case`: the agent's root writes). CI never runs them: they take the fully patched Yocto source tree, which CI does not have, and their `*-test.py` names are not collected by its pytest run; `docs/reference/patch-set.md` lists them for a manual run. Decide per check whether the code or the check is wrong, and give the series a CI job that patches the pinned upstream source and runs every check | Every check in `patch-set.md` passing on the patched tree, in that CI job |

Larger appliance/inventory refactors are not prerequisites for operating the
current fixed-pool lab. Start with a demonstrated defect and a bounded test,
not another broad architecture proposal. Keep new work items small, assign an
owner and acceptance gate, and remove them when completed. Historical detailed
plans and measurement narratives remain available through Git history.
