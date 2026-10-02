# easymesh-labs: the umbrella and workspace of the EasyMesh labs

<!-- labs block: the same in every repository of the EasyMesh labs, but for the Site line -->
**Site:** <https://mesh.vcpe.dev/> (this umbrella).
The [EasyMesh labs](https://mesh.vcpe.dev/) serve three
goals: EasyMesh optimizer development
([easymesh-optimizer](https://vcpe.dev/easymesh-optimizer/)) in a rich
virtual lab, on both stacks
([RDK EasyMesh](https://vcpe.dev/meta-cmf-bananapi-vcpe/),
[prplMesh](https://vcpe.dev/prplmesh-lab/)); unchanged OpenSync
pods as EasyMesh agents under a local controller, without the OpenSync cloud
([EMOSA](https://vcpe.dev/emosa-lab/), with the
[OpenSync lab](https://vcpe.dev/opensync-lab/)'s pods); and
EasyMesh on physical hardware
([Protocol lab](https://vcpe.dev/easymesh-lab/)). Two core
components carry them: the RF medium
([easymesh-medium](https://vcpe.dev/easymesh-medium/)) and EMOSA's
OVSDB ⇄ EasyMesh conversion. The rest is infrastructure, tools (the
[room builder](https://vcpe.dev/easymesh-room-builder/)) and learning
around them.
<!-- /labs block -->

This repository ties the projects together: the landing site, the manifest that pins
every project and the images the labs run, the workspace scripts that clone and pin
them, the plan that aligns them, and the files every project's site shares (the labs
bar, the Pages workflow, the documentation check).

## Components

| Project | Role | What it is |
| --- | --- | --- |
| [easymesh-medium](https://vcpe.dev/easymesh-medium/) | core | the RF medium: virtual radios, wmediumd and its patches, the rooms, the console, the controller's topology page |
| [emosa-lab](https://vcpe.dev/emosa-lab/) | core | EMOSA: unchanged OpenSync pods as EasyMesh agents; a Python reference and a C implementation |
| [easymesh-optimizer](https://vcpe.dev/easymesh-optimizer/) | optimizer | the steering optimizer both virtual labs run, and its room service |
| [easymesh-clients](https://vcpe.dev/easymesh-clients/) | shared | the labs' Wi-Fi clients: what each lab runs and how it builds and manages them, and how they can do more; documents only, each lab still creates its own |
| [easymesh-remote](https://vcpe.dev/easymesh-remote/) | shared | remote access to a lab: the gateway with its login and one reservation, how a host is set up, what each lab publishes |
| [meta-cmf-bananapi-vcpe](https://vcpe.dev/meta-cmf-bananapi-vcpe/) | lab | RDK-B on Banana Pi images in containers: the RDK EasyMesh lab; EMOSA as an option |
| [prplmesh-lab](https://vcpe.dev/prplmesh-lab/) | lab | the same lab on native prplMesh |
| [opensync-lab](https://vcpe.dev/opensync-lab/) | lab | a representative OpenSync router and the OpenSync pod image; EMOSA's reference lab |
| [easymesh-lab](https://vcpe.dev/easymesh-lab/) | learning | the protocol on certified hardware: a from-scratch controller and a teaching panel |
| [easymesh-room-builder](https://vcpe.dev/easymesh-room-builder/) | tool | design the labs' rooms in the browser, compiled to the medium's world plans |
| [easymesh-resources](https://vcpe.dev/easymesh-resources/) | shared | shared material: the MV3 EasyMesh footprint and the production plan |

In this repository: `site/` (the landing page and the posters), `manifest.json`, `sync`
and `pin`, `docs/`, and `pages/` with `.github/workflows/pages.yml` (shared by every
project's site).

## Getting started

```sh
git clone git@github.com:boardfarmdevs/easymesh-labs.git ~/git/easymesh-labs
cd ~/git/easymesh-labs
./sync             # clone or fast-forward the projects into this directory
./sync --pinned    # or: check out the commits manifest.json pins
./pin              # record the commits in use as the new pins (clean and pushed only)
```

`manifest.json` lists the projects, their goal, branch and pinned commit, and the
images the labs run that are built outside a lab VM (the OpenSync pod image, the
Banana Pi images) with the commit each was built from. The projects are cloned next
to it and ignored by this repository. `./sync` never discards work: a project with
local changes, its own commits or on another branch is left as it is. Build trees and
caches (Yocto, downloads, sstate) stay outside the workspace; each project's guide
says where. The room builder is not cloned.

## Documentation

The [site](https://mesh.vcpe.dev/) says what the labs are for and
links every project; its two posters show where everything lives and the labs as built.
The documents are indexed in [docs/README.md](docs/README.md): the lab configurations and
the VMs that run now, the alignment plan and its status, and the open proposals.
