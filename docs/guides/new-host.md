# Setting up a new lab host

[Documents](../README.md)

**Kind:** guide. **Written:** 8 October 2026, with a GMKtec NucBox K8 as the worked example
([below](#the-worked-example-a-nucbox-k8)).

From a bare machine to qualified labs: what the host must have, the role it takes, the base
system, LXD and its storage, the workspace, the artifacts, each lab built and qualified,
remote access, and the physical parts. Each step says where its commands run and links the
project guide that holds the detail; this guide puts them in order and does not repeat them.

## 1. Know the host

Run this **on the new host**, in a terminal there; it only reads, and saves to
`~/new-machine-specs.txt`:

```sh
{
echo "== host";    hostnamectl 2>/dev/null || hostname
echo "== os";      grep -E '^(PRETTY_NAME|VERSION_ID)=' /etc/os-release; uname -r
echo "== cpu";     lscpu | grep -E 'Model name|^CPU\(s\)|Thread\(s\)|Core\(s\)|Socket\(s\)|Virtualization|L3'
echo "== kvm";     ls -l /dev/kvm 2>&1
echo "== memory";  free -h
echo "== disks";   lsblk -d -o NAME,SIZE,ROTA,TRAN,MODEL
echo "== filesystems"; df -hT -x tmpfs -x devtmpfs -x squashfs -x overlay
echo "== network"; ip -br link; ip -br addr; ip route | head -3
echo "== usb";     lsusb 2>/dev/null
echo "== tools";   for t in snap lxd lxc docker zfs git python3 uv tailscale; do printf '%-10s %s\n' "$t" "$(command -v $t || echo missing)"; done
snap list 2>/dev/null | grep -E '^(lxd|core)'
} 2>&1 | tee ~/new-machine-specs.txt
```

Compare it with what each use needs:

| Use | CPU | Memory | Disk | Also |
| --- | --- | --- | --- | --- |
| One lab VM (RDK, prplMesh, OpenSync + EMOSA) | 8 threads for the VM | 16 GiB given to the VM (about 11 used, with free page reporting) plus the host's own and the ZFS cache | a 96 GiB disk each in the `labs` pool, sparse: about 7 GB used by an RDK lab; snapshots and copies share blocks | `/dev/kvm`; one lab running, building or testing at a time per host |
| The RDK lab's Banana Pi images from scratch (Yocto) | as many as possible | 32 GiB recommended | 300 GiB for the tree, downloads, sstate and images | RDK Central's credentials; GNU tar 1.34 (the RDK build guide) |
| The prplMesh lab's native artifacts | 8 cores | 24 GiB | 240 GiB plus the build | |
| The OpenSync lab's mv3 container image | as above | as above | its mirror and reference build (tens of GiB) | the operator's MV3 sources (see step 7) |
| The Pi pods' bench | modest | modest | a few GiB | the Pis on its LAN, their serial consoles |

## 2. Decide its role and its place on the network

| Role | What runs there | Needs |
| --- | --- | --- |
| **Lab host from prebuilt artifacts** (the usual) | lab VMs built from images and base VMs other hosts built | the lab LAN, for the artifact store on rev140 |
| **Full build and lab host** | everything, including Yocto builds | the memory and disk of a build host (step 1), RDK Central's credentials |
| **Pi bench host** | the Pi pods' bench and builds (opensync-rpi) | the Pis and their serial consoles on its LAN |
| **Workstation** | the repositories, the room builder, the sites, ssh to the hosts | nothing beyond git and Python |

**On the network:** the lab hosts, the console server and the artifact store
(`http://192.168.2.140:8180`) are on the lab LAN, 192.168.2.0/24, which the store serves only.
A host on another network can reach the labs only through remote access (step 9) and must
build what it cannot fetch. Put a lab host on the lab LAN, wired, as its default route.

**What is already on the host:** other labs' Docker or LXD bridges and their address ranges
may overlap the labs' networks (LXD's bridges, the VMs' inner 10.x networks). List them
(`ip -br addr`, `lxc network list`, `docker network ls`) and decide what stays before
installing anything.

## 3. The base system

**On the new host:**

1. **Ubuntu 22.04 or 24.04**, x86-64, with the HWE kernel (6.8 or later). The lab VMs bring
   their own kernel 7.0; the host's matters only for KVM and ZFS.
2. **Firmware (BIOS):** virtualization on (`AMD-V`/SVM or VT-x). On a mini PC with an
   integrated GPU, set the GPU's reserved memory (UMA frame buffer) to its minimum: it is
   taken from the RAM the labs get.
3. **The account:** the labs run as your normal user with passwordless `sudo` (the scripts
   say when they need root), and the room tests reach the host's LXD over `ssh localhost`
   without a password. The `sudo` rule goes in a file of its own, checked by `visudo` before
   it is installed (a broken sudoers file locks `sudo` out):

   ```sh
   echo "$USER ALL=(ALL) NOPASSWD: ALL" > /tmp/nopasswd
   sudo visudo -cf /tmp/nopasswd && sudo install -m 0440 /tmp/nopasswd "/etc/sudoers.d/90-$USER-nopasswd"
   sudo -k && sudo -n true && echo sudo-ok     # no password asked

   sudo apt install -y openssh-server
   test -f ~/.ssh/id_ed25519 || ssh-keygen -t ed25519 -N '' -f ~/.ssh/id_ed25519
   grep -qxF "$(cat ~/.ssh/id_ed25519.pub)" ~/.ssh/authorized_keys 2>/dev/null ||
       cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ssh -o StrictHostKeyChecking=accept-new localhost true && echo ssh-ok
   ```
4. **Git access:** an SSH key on GitHub with access to the boardfarmdevs repositories (some
   are private), and on the hosts you work with (`ssh-copy-id rev@rev140` and so on).
5. **Never asleep:** a desktop install suspends when idle, which stops a running lab or a
   build (`systemd-inhibit` from an SSH session is refused). Turn sleep off for good:
   `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`.
6. **Time and name:** NTP on (`timedatectl`), and a hostname in the lab's naming (`revNNN`)
   if it joins the lab hosts.
7. **Basic tools:**

   ```sh
   sudo apt update && sudo apt install -y git curl zstd python3-venv qemu-kvm snapd
   sudo snap install astral-uv --classic     # uv, which several projects' Python tools and tests use
   sudo apt install -y libnl-3-dev libnl-genl-3-dev libconfig-dev pkg-config   # the RDK lab's VM builder compiles wmediumd here
   sudo snap install go --classic            # and the medium's console, which needs Go 1.22 or later (22.04's own is 1.18)
   ```

## 4. LXD and its storage

**On the new host**, in the RDK lab's checkout, which the workspace puts in
`~/git/easymesh-labs/meta-cmf-bananapi-vcpe` (do step 5 first if it is not there):

```sh
cd ~/git/easymesh-labs/meta-cmf-bananapi-vcpe
sudo gen/vm/lxd/install-host.sh       # Ubuntu, KVM, the LXD snap, your user in the lxd group
sudo snap refresh lxd --channel=6/stable && sudo snap refresh --hold lxd    # as on every lab host
test -c /dev/kvm && groups | grep -qw lxd && echo ready    # no "ready": log out and in again
```

Then the host's one ZFS pool for lab VMs, `labs` (the lab configurations reference,
[Storage](../reference/lab-configurations.md#storage)): the labs' builds create it when it is
missing, or create it now. Its size is a cap on a sparse loop file, not space taken: a lab
host's pool holds 5 to 6 GiB with a lab running (compressed), and Yocto builds on the same
disk need about 300 GiB, so keep the cap small and grow it when needed
(`lxc storage set labs size=300GiB`):

```sh
lxc storage create labs zfs size=200GiB      # room for every virtual lab and its snapshots
printf 'options zfs zfs_arc_max=%s\n' 3221225472 | sudo tee /etc/modprobe.d/zfs.conf   # ZFS's cache: 3 GiB under 32 GiB of RAM, 8 GiB on 64
echo 3221225472 | sudo tee /sys/module/zfs/parameters/zfs_arc_max
```

The ZFS tools come with the LXD snap; the host needs only Ubuntu's ZFS module.

**If Docker is installed on the host**, check that it leaves forwarding alone. Docker sets
the firewall's FORWARD policy to DROP when it is the one to turn IP forwarding on, and LXD's
bridge is then cut off: a lab VM resolves names but reaches nothing, and the VM build stops at
its first `apt-get` ("Unable to locate package docker.io"). Docker 28 or later has an option
for it; the lab hosts run with the policy at ACCEPT:

```sh
sudo iptables -S FORWARD | head -1          # "-P FORWARD DROP": fix it
printf '{\n  "ip-forward-no-drop": true\n}\n' | sudo tee /etc/docker/daemon.json   # merge by hand if the file exists
sudo systemctl restart docker && sudo iptables -P FORWARD ACCEPT
```

## 5. The workspace

**On the new host:**

```sh
git clone git@github.com:boardfarmdevs/easymesh-labs.git ~/git/easymesh-labs
cd ~/git/easymesh-labs
./sync --pinned        # every project at the commit manifest.json pins
```

Build trees and caches stay outside the workspace: Yocto trees under `~/yocto`, shared
downloads and sstate under `~/oe/downloads` and `~/oe/sstate-cache`. The room builder, the
resources, the clients' documents and the remote access gateway are separate repositories;
clone them where you need them.

## 6. Artifacts: fetch or build

**Only on the lab LAN** (192.168.2.0/24), fetch what other hosts built, by its inputs
([the artifact store](../reference/artifact-store.md)). Off it, skip this block: those
addresses are unreachable, and the exports would replace the host's own store below.

```sh
export EASYMESH_ARTIFACT_STORE=http://192.168.2.140:8180
export BUILD_SSTATE_MIRROR=http://192.168.2.140:8180/sstate-cache    # Yocto: minutes instead of hours
```

Off the lab LAN, build them. First the host setup of the RDK lab's
[build guide](https://vcpe.dev/meta-cmf-bananapi-vcpe/) (`docs/guides/build.md`): its packages
(`gcc-multilib` among them), `repo`, and GNU tar 1.34 (the build refuses a tar that uses
`openat2`). Then RDK Central's login, and the images, in a clone of the RDK lab of its own at the
workspace's pin, inside `tmux` so the build outlives a dropped SSH session (detach with Ctrl-b
then d, come back with `tmux attach -t bpi`).

The host keeps its own [artifact store](../reference/artifact-store.md), a directory: each
build publishes its image there under the key of its inputs, and a later build with the same
inputs takes it from there. The store is what keeps the images: the controller and the EMOSA
controller image are one machine, so building one removes the other from the build's deploy
folder. The checkout is on a local branch, `pinned`, because the lab VM's builder names the
VM's copy of it after the branch.

```sh
printf 'machine code.rdkcentral.com login USER password TOKEN\n' > ~/.netrc && chmod 600 ~/.netrc
git config --global color.ui auto            # or repo init stops to ask
sudo apt install -y tmux && tmux new -s bpi

export EASYMESH_ARTIFACT_STORE=$HOME/artifacts EASYMESH_ARTIFACT_PUBLISH=$HOME/artifacts
pin=$(git -C ~/git/easymesh-labs/meta-cmf-bananapi-vcpe rev-parse HEAD)
mkdir -p ~/yocto/easymesh-bpi && cd ~/yocto/easymesh-bpi
git clone git@github.com:boardfarmdevs/meta-cmf-bananapi-vcpe.git && cd meta-cmf-bananapi-vcpe
git checkout -B pinned "$pin" && git submodule update --init --recursive
{ bash gen/build/bootstrap-sources.sh && bash gen/build/build-images.sh both; } 2>&1 | tee ~/bpi-build.log
BUILD_EMOSA=1 bash gen/build/build-images.sh controller 2>&1 | tee ~/bpi-emosa.log    # for the RDK lab + EMOSA
```

From scratch on 16 threads the controller image takes about two hours (the sources'
download included); the extender and the EMOSA controller image then reuse it and take
minutes (on the K8, 9 October: the EMOSA controller image 3 min 19 s, the controller and
the extender together 3 min 58 s). While it runs, and when it is done:

```sh
grep -o 'Running task [0-9]* of [0-9]*' "$(ls -td ~/yocto/easymesh-bpi/build-evidence/*/ | head -1)"build.log | tail -1
for r in controller extender controller-emosa; do R=$(cat ~/yocto/easymesh-bpi/build-evidence/latest-$r)
  echo "$r: exit $(cat "$R/exit-code")"; ls ~/artifacts/store/rdk-image-$r/"$(cat "$R/image-key")"/*.lxc.tar.bz2; done
```

Each image should show exit 0 and its file in the store. An image built before the store was
set up is published by running its build again with the two exports: its inputs are
unchanged, so it takes minutes. A build that stops partway resumes when run again; one image
alone is `build-images.sh controller` or `extender`. A fetch that fails once on `server certificate
verification failed` is the network: run it again. The first build fills `~/oe`; later
ones reuse it. The prplMesh lab's build guide has its native artifacts
(`deploy/lxd-vm/build-artifacts.sh`).

## 7. The labs, one at a time

A host runs, builds or tests one lab at a time: lab VMs sharing a host lose packets in their
traffic checks. Each lab's site has its build and VM guides.

| Lab | Built with (on the new host) | Its guide |
| --- | --- | --- |
| **RDK EasyMesh lab** | `bash gen/build/build-images.sh both` (or fetched), then `EASYMESH_CONTROLLER_IMAGE=... EASYMESH_EXTENDER_IMAGE=... gen/vm/lxd/build.sh build`; about an hour | [meta-cmf-bananapi-vcpe](https://vcpe.dev/meta-cmf-bananapi-vcpe/): the build and VM guides |
| **RDK lab + EMOSA**, the target configuration | the same build with `EASYMESH_EMOSA=1 EASYMESH_EMOSA_IN=gateway` and a controller image built with `BUILD_EMOSA=1`; about 90 minutes | the same, "The EMOSA option"; [emosa-lab](https://vcpe.dev/emosa-lab/) |
| **prplMesh lab** | `deploy/lxd-vm/build-artifacts.sh`, then `deploy/lxd-vm/build.sh build` | [prplmesh-lab](https://vcpe.dev/prplmesh-lab/) |
| **OpenSync lab** | `./build-mvx.sh pin` and `build` (the operator's MV3 sources: its repo mirror under `~/yocto/repo_reference` and the reference build, today only on rev140, copied over), `./setup-vm.sh all`, `./deploy-mvx.sh all`, `./build-pod.sh all`, `./deploy-mvx.sh mesh` | [opensync-lab](https://vcpe.dev/opensync-lab/) |
| **OpenSync + EMOSA** | the OpenSync lab, then emosa-lab's `deploy/opensync-lab/lab.sh` | [emosa-lab](https://vcpe.dev/emosa-lab/) |
| **Physical protocol lab** | easymesh-lab's VM (`deploy/lxd-vm/build_vm.py`) and its hardware: the extenders and the USB Wi-Fi clients handed to it | [easymesh-lab](https://vcpe.dev/easymesh-lab/) |

Name each VM after its configuration and date (the lab configurations reference), and keep
the configurations reference's hosts table current.

The RDK lab from the images built in step 6, in `tmux`, about an hour. The images come from
the host's store, by the key each build recorded; the VM builder keeps its base VM there too.
Its first stage compiles the medium's `wmediumd` and console on the host: without step 3's
libnl, libconfig and Go it stops within seconds ("Cannot find development files for any
supported version of libnl", "go: command not found").

```sh
cd ~/yocto/easymesh-bpi/meta-cmf-bananapi-vcpe
export EASYMESH_ARTIFACT_STORE=$HOME/artifacts EASYMESH_ARTIFACT_PUBLISH=$HOME/artifacts
source gen/build/lab-config.sh "rdk-$(date -u +%m%d)"       # the VM's name and its ports
image() { ls ~/artifacts/store/rdk-image-"$1"/"$(cat "$(cat ~/yocto/easymesh-bpi/build-evidence/latest-"$1")/image-key")"/*.lxc.tar.bz2; }
controller=$(image controller) && extender=$(image extender) && ls -l "$controller" "$extender"
CLIENT_CREATE_PARALLELISM=8 EASYMESH_CONTROLLER_IMAGE="$controller" EASYMESH_EXTENDER_IMAGE="$extender" \
  gen/vm/lxd/build.sh build 2>&1 | tee ~/rdk-vm-build.log
```

It ends by printing the lab's web addresses (topology, room, wmediumd console). On the K8 (9
October, `rdk-1009`) it took 56 minutes, most of it the mesh (9 min), the 100 clients
(12.5 min) and the cold boot (14 min); the acceptance's health audit passed, and the VM used
3.4 GiB of the `labs` pool and 7.3 GiB of memory.

## 8. Qualify each lab

A build's acceptance is not the qualification. Run each lab's suite before calling it a
lab: the RDK lab's `gen/tests/run-easymesh-suite.sh all --yes-act`, the prplMesh lab's
`tests/run-prplmesh-suite.sh all`, with the room browser on another host where the guides
say so. The suites take hours; nothing else runs on the host meanwhile. The RDK lab's `all`
includes its 12-hour soak.

The RDK lab's suite needs, on the host (its [test guide](https://vcpe.dev/meta-cmf-bananapi-vcpe/),
`docs/guides/test-suite.md`): step 3's passwordless `ssh localhost`, a Python environment
with its requirements, and Node 22 or later. On Ubuntu 22.04 the Node snap fails (built for a
newer glibc), and nodejs.org's own build works. The lab's web proxies listen on the host's
address, not loopback, so the suite is told that address. In `tmux`:

```sh
f=$(curl -fsS https://nodejs.org/dist/latest-v24.x/SHASUMS256.txt | grep -o 'node-v24[0-9.]*-linux-x64.tar.xz' | head -1)
curl -fsSL "https://nodejs.org/dist/latest-v24.x/$f" | tar -xJ -C ~/.local/opt     # mkdir -p ~/.local/opt first
for b in node npm npx; do ln -sf ~/.local/opt/"${f%.tar.xz}"/bin/$b ~/bin/$b; done

cd ~/yocto/easymesh-bpi/meta-cmf-bananapi-vcpe
python3 -m venv ~/.venvs/easymesh-tests && source ~/.venvs/easymesh-tests/bin/activate
python3 -m pip install -r gen/tests/requirements.txt
source gen/build/lab-config.sh rdk-MMDD                  # the lab's name
export EASYMESH_HOST_ADDRESS=$(lxc config device show "$EASYMESH_LXD_NAME" | awk '/listen: tcp:/ {split($2, a, ":"); print a[2]; exit}')
python3 gen/medium/observer/check-ready.py --url "http://$EASYMESH_HOST_ADDRESS:$WMEDIUMD_CONSOLE_PORT" --require-room --require-survey
gen/tests/run-easymesh-suite.sh all --yes-act --install-browser-deps 2>&1 | tee ~/suite.log
```

The results are under `test-results/<time>/` in the checkout (`results.tsv`, `summary.json`);
a skipped or blocked section is not a pass. A host whose address comes from DHCP (the K8's
Wi-Fi) keeps the lab reachable only while that address holds.

## 9. Remote access

To reach a lab from outside the lab LAN, install the gateway on the host and give the lab a
Tailscale name of its own: [easymesh-remote](https://vcpe.dev/easymesh-remote/)'s setup
guide (`manage.py configure`, `address`, `publish --mode private`). Labs start private;
public access is the owner's decision.

## 10. Physical parts, if the host has them

- **USB Wi-Fi adapters (MT7921AU):** they first appear in their driver-disk mode
  (USB ID `0e8d:c616`); `usb-modeswitch` turns them into the radio (`0e8d:7961`). The Pi
  pods' setup guide ([opensync-rpi](https://vcpe.dev/opensync-rpi/)) installs it.
- **Serial consoles** (an FT232 cable or the lab's console server): the way back to a board
  or a Pi when its network is changed.
- **The Pi pods' bench:** opensync-rpi's guides, on a host on the same LAN as the Pis.

## 11. Done when

- `lxc storage list` shows `labs`, `snap refresh --time` shows LXD held, `/dev/kvm` exists.
- The workspace is at the pins (`./sync --pinned` clean).
- Each lab the host runs has passed its suite, and the lab configurations reference names
  the host and its VMs.
- Its labs are reachable as intended: on the lab LAN, or through the gateway.

## The worked example: a NucBox K8

Read on 8 October 2026 with step 1's command.

| | |
| --- | --- |
| Machine | GMKtec NucBox K8, a mini PC |
| CPU | AMD Ryzen 7 8845HS, 8 cores and 16 threads, AMD-V; `/dev/kvm` present |
| Memory | 28 GiB visible (probably 32 GB fitted, the rest reserved for the Radeon 780M), 2 GiB swap |
| Disk | 1 TB NVMe (Lexar NM7A1), one ext4 filesystem, 751 GB free |
| System | Ubuntu 22.04.5, kernel 6.8 |
| Network | two Ethernet ports (one on 192.168.4.0/24, one unused) and Wi-Fi (the default route); not on the lab LAN |
| Already there | another lab's Docker and LXD bridges (172.17-26.x, 10.20-22.x, 192.168.3.x, and LXD bridges in 10.139.x and 10.10.10.x) |
| USB | a MediaTek Wi-Fi adapter in its driver-disk mode, an FT232 serial cable |
| Tools | LXD 6.6 on 6/stable, Docker; no uv, no Tailscale; ZFS through the LXD snap |

What follows for it:

- **Compute and disk** match rev150's (a Ryzen 7 8745HS with 25 GiB): one lab VM at a time,
  with room to spare once a VM keeps only what it uses. A Yocto build from scratch beside a
  running lab is tight; fetch the images instead (step 6).
- **Memory:** lower the GPU's reserved memory in the firmware to get most of the 32 GB back.
  Then ZFS's cache at 3 GiB (step 4).
- **Network:** it is not on the lab LAN, so the artifact store, the console server and the
  other hosts are out of reach. Either cable it to the lab LAN as its default route, or keep
  it where it is, build everything itself and reach its labs through remote access.
- **The other lab on it:** decide whether it stays. If it does, check its address ranges
  against the labs' before the first lab VM.
- **The Wi-Fi adapter and the serial cable** suggest a Pi bench role as well (step 10).
- **LXD:** refresh to the version the other hosts run and hold it (step 4).
