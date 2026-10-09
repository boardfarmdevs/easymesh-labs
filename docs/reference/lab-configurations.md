# Lab configurations

The projects build six VM lab configurations. Four come from one project each; two add
EMOSA to one of those. The sixth, the physical protocol lab, is the only one tied to
hardware: certified extenders and real clients on one host. Each build script names its
VM by default after the configuration and the date (`MMDD`); the VMs that run now are
named in one place only, the hosts table below.

| # | Configuration (VM name) | Built from | Purpose | Host |
| --- | --- | --- | --- | --- |
| 1 | **RDK EasyMesh lab** (`rdk-MMDD`) | meta-cmf-bananapi-vcpe: the Banana Pi images, then `gen/vm/lxd/build.sh build` | optimizer development on RDK: the gateway and controller (`bpibroadband`), 4 Wi-Fi extenders and 1 wired extender, 100 room clients, wmediumd, the interactive room | rev140 |
| 2 | **prplMesh lab** (`prpl-MMDD`) | prplmesh-lab: `deploy/lxd-vm/build-artifacts.sh`, then `deploy/lxd-vm/build.sh build` | the same optimizer lab on native prplMesh, with a wired Agent | rev140 |
| 3 | **OpenSync lab** (`opensync-lab-MMDD`) | opensync-lab: the mv3 and pod images, then `setup-vm.sh all`, `deploy-mvx.sh all` and `deploy-mvx.sh mesh` | a representative router (mv3), OpenSync pods with virtual radios and clients, local-noc as their cloud | none on its own: the base of #4 |
| 4 | **OpenSync + EMOSA, prplMesh controller** (`emosa-osl-MMDD`) | #3, then emosa-lab `deploy/opensync-lab/lab.sh` (`stage`, `controller`, `emosa`, `fleet`, `admit`, `policy`, `gtp`, `option1`) | adapter development against a prplMesh controller: several pods, the 900-second fault workload, the EasyMesh wireless backhaul | rev150 |
| 5 | **RDK lab + EMOSA** (`rdk-emosa-MMDD`) | #1 with the EMOSA option: `EASYMESH_EMOSA=1 gen/vm/lxd/build.sh build` (or `build.sh emosa` on an accepted VM), which runs emosa-lab at the commit the RDK lab pins | OpenSync pods as agents next to the RDK lab's native agents, in the standard rooms with the pods | rev120 |
| 6 | **Physical protocol lab** (`easymesh-lab`) | easymesh-lab: `deploy/lxd-vm/build_vm.py`, then the USB handover (the Ethernet adapter to the extender, the USB Wi-Fi clients) | the EasyMesh protocol on certified hardware: a from-scratch controller and teaching panel, a TP-Link RE653BE and a second extender, real clients | rev120 |

Each project's site links its build guide: the RDK lab's for #1 and #5, prplmesh-lab's
for #2, opensync-lab's for #3, emosa-lab's for #4 and #5, easymesh-lab's for #6.
`manifest.json` pins the projects and the images built outside a lab VM (the OpenSync pod
image, the Banana Pi images) with the commit each was built from; a fresh build at the
pins gives what the running VMs have.

## Hosts

| Host | Runs |
| --- | --- |
| rev140 | the Yocto builds (mv3, OpenSync pod, Banana Pi images); `rdk-1004` (#5 in its target configuration, EMOSA wholly in the gateway; a prplMesh lab is built here when needed), one lab running, building or testing at a time (their builds and checks refuse while the other runs); any other long build on this host runs at low priority (`nice -n 19 ionice -c3`) while a lab VM is up |
| rev150 | no lab VM (`rdk-emosa-1006` removed 8 October); the room browser for the labs on rev140 and rev120, container builds and fuzzing |
| rev120 | `rdk-emosa-1005` (#5, the target configuration) and `easymesh-lab` (#6, stopped), whose physical devices are attached to rev120: physical tests run there. No prplMesh VMs or builders |
| rev-NucBox-K8 | the reference lab, at another site and off the lab LAN, everything built from scratch there ([new host guide](../guides/new-host.md)): `rdk-1009` (#1), built 9 October, its suite not yet run. Virtual labs only |

## Storage

Every host keeps its lab VMs in one ZFS pool, `labs`: snapshots and copies are
copy-on-write and take seconds, a lab and its copies share blocks, every block is
compressed. The labs' builds put a new VM there by default (the RDK lab
`EASYMESH_LXD_STORAGE`, the prplMesh lab `PRPLMESH_LXD_STORAGE`, the OpenSync lab
`MVX_VM_STORAGE`; easymesh-lab takes `--pool labs`); a lab built earlier stays in its own
`dir` pool until it is moved. Why, and what every lab VM keeps on disk:
[easymesh-resources lab-storage](https://vcpe.dev/easymesh-resources/lab-storage/).

The procedure on a host (done on rev120, rev140 and rev150 on 7 October 2026), between
room suites:

```sh
lxc storage create labs zfs size=500GiB    # a sparse loop file; rev140 1TiB. LXD sets compression=on
printf 'options zfs zfs_arc_max=%s\n' 8589934592 | sudo tee /etc/modprobe.d/zfs.conf    # ZFS's cache: 8 GiB; rev150 3221225472 (3 GiB)
echo 8589934592 | sudo tee /sys/module/zfs/parameters/zfs_arc_max    # the same, at once
sudo snap refresh --hold lxd                 # LXD updated on purpose only (6/stable on every host)
```

Grow the pool with `lxc storage set labs size=`; a lab moves into it stopped, with
`lxc move VM --storage labs` (its name and ports stay). The ZFS tools are the LXD snap's
(the hosts have the module, not always the tools): `sudo nsenter
--mount=/run/snapd/ns/lxd.mnt -- env LD_LIBRARY_PATH=/snap/lxd/current/zfs-2.2/lib:/snap/lxd/current/lib
/snap/lxd/current/zfs-2.2/bin/zfs get compressratio labs` (rev120 `zfs-2.4`).

## Reaching a lab

Each lab VM publishes its web interfaces as ports on its host, on the lab network. Which
interfaces each configuration has, and how a lab is reached from outside the lab network
(the gateway, with a login and one reservation), is in
[easymesh-remote](https://vcpe.dev/easymesh-remote/). The gateway serves the RDK lab's
layout (#1 and #5) today.

## Not (yet) a configuration

- **The combined end-goal system on a physical router**: one controller, native agents and
  OpenSync pods, EMOSA in the router's own image. #5 is that in the virtual lab, EMOSA
  wholly in the gateway image (its target configuration, `EASYMESH_EMOSA_IN=gateway`);
  on the physical mv3 it is phase 10 of [the alignment plan](../project/alignment-plan.md).
- **EMOSA in the prplMesh lab** (#2 with EMOSA): never built.
