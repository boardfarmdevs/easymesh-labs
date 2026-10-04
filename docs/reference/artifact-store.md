# The artifact store

[Documents](../README.md)

**Kind:** reference. **Since:** 3 October 2026, from the
[faster, cheaper labs](../proposals/faster-labs.md) proposal (its items 5 and 6).

What takes long to build and changes rarely is built once per set of inputs and kept,
so that a build on any host fetches what any host already built: the RDK lab's Banana Pi
images, the prplMesh lab's native archives, the labs' base VM images. A second service on
the same server shares rev140's Yocto caches.

## The server

| | |
| --- | --- |
| Where | rev140, `http://192.168.2.140:8180/`; a static, read-only HTTP server (`easymesh-artifacts.service`), at low CPU and I/O priority |
| What it serves | `/srv/easymesh-artifacts`: `store/` (the entries), `sstate-cache/` and `downloads/` (links to `~/oe/sstate-cache` and `~/oe/downloads`) |
| Installed by | `sudo artifacts/install-server.sh` in this repository (`--port`, `--root`, `--sstate`, `--downloads`) |
| Access | the lab network only; anyone on it can read, and only accounts on the store host (or with ssh to it) can publish |

## An entry

`store/COMPONENT/KEY/`: the artifact's files, `SHA256SUMS` over them, and
`provenance.env` (what it was built from, when, where). `KEY` is 16 hex digits of a digest
over every input that decides the artifact, so a change to any input is a new key and an
unchanged one finds the old artifact. A fetch checks every file against `SHA256SUMS` and
refuses a mismatch; a publish writes the entry under a temporary name and renames it, so
a reader never sees half of one.

| Component | Built by | Its key covers |
| --- | --- | --- |
| `rdk-image-controller`, `rdk-image-extender`, `rdk-image-controller-emosa` | the RDK lab's `gen/build/build-images.sh` | the manifest (every upstream layer's pin), the layer's recipes, classes, configuration and build files, the medium's topology page and the viewer modules it shares, and for EMOSA its pin |
| `rdk-base-vm` | the RDK lab's `gen/vm/lxd/build.sh` | the base stages' scripts and service files, the kernel, the medium's radio module, Boardfarm's commit, the radio count |
| `prplmesh-native` | the prplMesh lab's `deploy/lxd-vm/build-artifacts.sh` | the pinned prplMesh and hostap revisions, the native build scripts and every patch (`deploy/lxd-vm/native-inputs.sh`) |
| `prplmesh-client` | the prplMesh lab's `scripts/build-client-artifact.sh` | the Alpine clients' supplicant: the pinned hostap revision, its patches, the build script, the Alpine image |
| `prplmesh-base-vm` | the prplMesh lab's `deploy/lxd-vm/build.sh` | the VM image, the kernel, the base packages and the guest functions that install them |

## Using it

| Variable | Meaning |
| --- | --- |
| `EASYMESH_ARTIFACT_STORE=http://192.168.2.140:8180` | fetch from the store; unset, nothing is fetched and everything is built |
| `EASYMESH_ARTIFACT_PUBLISH=/srv/easymesh-artifacts` | publish what a build made, on the store host; from another host `rev140:/srv/easymesh-artifacts` (rsync over ssh); unset, nothing is published |
| `BUILD_FORCE=1` | build even when the store has the entry |
| `BUILD_SSTATE_MIRROR=http://192.168.2.140:8180/sstate-cache` | the RDK image build fetches sstate objects from rev140 before building them: a host without a warm cache builds in minutes instead of hours |

The client is a few shell functions, `artifact_key`, `artifact_fetch` and
`artifact_publish`, in each lab (`gen/build/artifact-store.sh` in the RDK lab,
`deploy/lxd-vm/artifact-store.sh` in the prplMesh lab), so a lab builds without this
repository.

## Keeping it

The store grows by an entry per new set of inputs. Entries are independent: removing a
directory under `store/` costs only a rebuild the next time those inputs are asked for.
Prune by age when the disk asks for it (`find /srv/easymesh-artifacts/store -mindepth 2
-maxdepth 2 -mtime +60`), never the entries the running labs were built from.
