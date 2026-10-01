# EasyMesh labs

<!-- labs block: the same in every repository of the EasyMesh labs, but for the Site line -->
**Site:** <https://boardfarmdevs.github.io/easymesh-labs/> (this umbrella).
The [EasyMesh labs](https://boardfarmdevs.github.io/easymesh-labs/) serve three
goals: EasyMesh optimizer development
([easymesh-optimizer](https://github.com/boardfarmdevs/easymesh-optimizer)) in a rich
virtual lab, on both stacks
([RDK EasyMesh](https://boardfarmdevs.github.io/meta-cmf-bananapi-vcpe/),
[prplMesh](https://boardfarmdevs.github.io/prplmesh-lab/)); unchanged OpenSync
pods as EasyMesh agents under a local controller, without the OpenSync cloud
([EMOSA](https://boardfarmdevs.github.io/emosa-lab/), with the
[OpenSync lab](https://boardfarmdevs.github.io/opensync-lab/)'s pods); and
EasyMesh on physical hardware
([Protocol lab](https://boardfarmdevs.github.io/easymesh-lab/)). Two core
components carry them: the RF medium
([easymesh-medium](https://github.com/boardfarmdevs/easymesh-medium)) and EMOSA's
OVSDB ⇄ EasyMesh conversion. The rest is infrastructure and learning around them.
<!-- /labs block -->

## What the project is for

- **Optimizer development in a rich virtual lab.** EasyMesh optimizer
  algorithms are developed against complete EasyMesh networks in containers:
  a gateway and controller, native extenders, a hundred Wi-Fi clients and
  interactive rooms that move them, all on one emulated radio medium. The same
  lab exists on both EasyMesh stacks, **RDK** and **prplMesh**.
- **EMOSA: OpenSync pods as they are, in an EasyMesh system.** Existing
  OpenSync pods, unchanged, run as EasyMesh agents under a local EasyMesh
  controller, with no OpenSync cloud.
- **A physical EasyMesh lab.** The protocol on certified hardware and real
  radios, which keeps the virtual labs honest.

## Two core components

Everything rests on two components. They get the most care, each has one
repository with its own specification and tests, and the labs consume them at
pinned commits.

| Component | Repository | What it must do |
| --- | --- | --- |
| **The RF medium** | [easymesh-medium](https://github.com/boardfarmdevs/easymesh-medium) | emulate the radio medium correctly for every lab: wmediumd and its patch series, the hwsim radios, the room language and the rooms, the medium's console |
| **EMOSA** | [emosa-lab](https://github.com/boardfarmdevs/emosa-lab) | the full conversion between OpenSync's OVSDB and EasyMesh, so that an unchanged pod is a complete EasyMesh agent; a Python reference and a C implementation that behave identically |

## Everything around them

The rest is **infrastructure** that builds and exercises the two components,
and **exploratory learning** that informs them.

| Role | Project | What it is |
| --- | --- | --- |
| the first goal's work: the optimizer | [easymesh-optimizer](https://github.com/boardfarmdevs/easymesh-optimizer) | the steering optimizer both virtual labs run, and the room service that runs it live: one policy core, an adapter per stack (RDK, prplMesh), its scenarios and manuals; both labs pin it (`gen/optimizer`, `optimizer`) |
| infrastructure: the RDK lab | [meta-cmf-bananapi-vcpe](https://github.com/boardfarmdevs/meta-cmf-bananapi-vcpe) | RDK-B on Banana Pi images in containers: controller, extenders, clients, the lab's rooms (manifests and bindings), the lab's suites; EMOSA as an option |
| infrastructure: the prplMesh lab | [prplmesh-lab](https://github.com/boardfarmdevs/prplmesh-lab) | the same lab on native prplMesh |
| infrastructure: OpenSync | [opensync-lab](https://github.com/boardfarmdevs/opensync-lab) | a representative OpenSync router (mv3) and the OpenSync pod image; with EMOSA, the adapter's reference lab |
| learning: the physical lab | [easymesh-lab](https://github.com/boardfarmdevs/easymesh-lab) | a from-scratch Python IEEE 1905.1/EasyMesh controller and teaching panel, driving certified extenders (a TP-Link RE653BE on Ethernet, a second extender onboarded through it onto a Wi-Fi backhaul) with real tri-band clients |
| tool | [easymesh-room-builder](https://github.com/boardfarmdevs/easymesh-room-builder) ([open it](https://boardfarmdevs.github.io/easymesh-room-builder/)) | a visual designer for the labs' rooms, compiled to the same world plans as the medium's configurator; not cloned by the workspace |

`easymesh-lab` (the physical lab) is one letter from this repository's name:
`easymesh-labs` is the umbrella and workspace.

## Where to start

| You want to | Start at |
| --- | --- |
| see every piece and where it lives, at a glance | the posters: [where everything lives](site/posters/map.html) and [the labs as built](site/posters/labs.html) ([on the site](https://boardfarmdevs.github.io/easymesh-labs/posters/map.html)) |
| develop or evaluate an optimizer | [easymesh-optimizer](https://github.com/boardfarmdevs/easymesh-optimizer) and its manuals; run it live in the RDK or the prplMesh lab (their sites); the rooms are the medium's; a change is requalified in both labs |
| change how radio is emulated | easymesh-medium: it builds and checks without a lab; a change is then requalified in both labs |
| work on EMOSA (or take it over) | emosa-lab: the specification, the design, the conformance vectors, then the implementations |
| know what runs where | [docs/lab-configurations.md](docs/lab-configurations.md) |
| follow the plan and its status | [docs/alignment-plan.md](docs/alignment-plan.md) |

## The workspace

```sh
git clone git@github.com:boardfarmdevs/easymesh-labs.git ~/git/easymesh-labs
cd ~/git/easymesh-labs
./sync             # clone or fast-forward the projects into this directory
./sync --pinned    # or: check out the commits manifest.json pins
./pin              # record the commits in use as the new pins (clean and pushed only)
```

`manifest.json` lists the projects, their goal, branch and pinned commit, and the
images the labs run that are built outside a lab VM (the OpenSync pod image, the
Banana Pi images) with the commit each was built from. The
projects are cloned next to it and ignored by this repository. `./sync` never
discards work: a project with local changes, its own commits or on another
branch is left as it is. Large build trees and caches (Yocto, downloads, sstate)
stay outside the workspace; each project's own guide says where.

How the simulated labs were last built again from this workspace is
[docs/fresh-build.md](docs/fresh-build.md). The six VM lab
configurations the projects build (the RDK and prplMesh labs, the OpenSync lab,
EMOSA on the OpenSync and on the RDK lab, and the physical protocol lab), their
purpose and their current VMs are in [docs/lab-configurations.md](docs/lab-configurations.md).
The plan that aligns the labs, up to carrying EMOSA in C in the RDK gateway image, and its
status is [docs/alignment-plan.md](docs/alignment-plan.md).
A proposal for offering the labs as a service to remote optimizer
developers (not implemented) is [docs/proposals/labs-as-a-service.md](docs/proposals/labs-as-a-service.md).

## The site

`site/` is the landing page. It is published like the lab projects' sites: the
shared `.github/workflows/pages.yml` runs `pages/build`, and
`pages/finish-site.py` adds the labs bar (`pages/labs-bar.js`) whose home link is
this site; first `pages/check-docs.py` checks the labs block and the links in
the Markdown. `pages/labs-bar.js`, `pages/finish-site.py`, `pages/check-docs.py`
and the workflow are the same in all six repositories (easymesh-medium and
easymesh-optimizer, without a site, run `pages/check-docs.py` in their checks);
change them in all.
