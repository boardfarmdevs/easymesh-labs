# EasyMesh labs

<!-- labs block: the same in the lab repositories -->
**Site:** <https://boardfarmdevs.github.io/easymesh-labs/>. The umbrella of the
boardfarmdevs labs, which serve three goals: the EasyMesh optimizer
([RDK EasyMesh](https://boardfarmdevs.github.io/meta-cmf-bananapi-vcpe/),
[prplMesh](https://boardfarmdevs.github.io/prplmesh-lab/)), the OpenSync adapter
([EMOSA](https://boardfarmdevs.github.io/emosa-lab/), [OpenSync](https://boardfarmdevs.github.io/opensync-lab/))
and EasyMesh on physical hardware ([Protocol lab](https://boardfarmdevs.github.io/easymesh-lab/)),
on the way to one EasyMesh system on wmediumd with native agents and OpenSync pods together.

This repository is the workspace for the five projects and the home of the work
that joins them.

| Goal | Project | What it is |
| --- | --- | --- |
| EasyMesh optimizer | [meta-cmf-bananapi-vcpe](https://github.com/boardfarmdevs/meta-cmf-bananapi-vcpe) | RDK-B on Banana Pi images in containers: EasyMesh, virtual RF and medium (wmediumd), optimizer, interactive room |
| EasyMesh optimizer | [prplmesh-lab](https://github.com/boardfarmdevs/prplmesh-lab) | The same lab on native prplMesh |
| OpenSync adapter | [emosa-lab](https://github.com/boardfarmdevs/emosa-lab) | EMOSA, the EasyMesh-to-OpenSync adapter: existing OpenSync pods as EasyMesh agents |
| OpenSync adapter | [opensync-lab](https://github.com/boardfarmdevs/opensync-lab) | A representative router (mv3) and OpenSync pods with virtual radios and clients |
| Physical EasyMesh | [easymesh-lab](https://github.com/boardfarmdevs/easymesh-lab) | A from-scratch Python IEEE 1905.1/EasyMesh controller and teaching panel, driving certified extenders (TP-Link RE653BE) with real tri-band clients: phones, tablets, laptops and managed USB Wi-Fi 7 clients |

**End goal:** one EasyMesh system on wmediumd, with native EasyMesh agents and
existing OpenSync pods (through EMOSA) side by side under one controller. The
physical lab keeps the simulated labs honest: the same protocol, on certified
devices and real radios. Its name is one letter from this repository's:
`easymesh-lab` is the physical lab, `easymesh-labs` the umbrella.

## The workspace

```sh
git clone git@github.com:boardfarmdevs/easymesh-labs.git ~/git/easymesh-labs
cd ~/git/easymesh-labs
./sync             # clone or fast-forward the five projects into this directory
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

The plan for building the four simulated labs again from this workspace, and which host
runs what, is [docs/fresh-build.md](docs/fresh-build.md). The six VM lab
configurations the projects build (the RDK and prplMesh labs, the OpenSync lab,
EMOSA on the OpenSync and on the RDK lab, and the physical protocol lab), their
purpose and their current VMs are in [docs/lab-configurations.md](docs/lab-configurations.md).
The plan that aligns the labs, up to carrying EMOSA in C in the RDK gateway image, and its
status is [docs/alignment-plan.md](docs/alignment-plan.md).
A proposal for offering the labs as a service to remote optimizer
developers (not implemented) is [docs/proposals/labs-as-a-service.md](docs/proposals/labs-as-a-service.md).

## The site

`site/` is the landing page. It is published like the five project sites: the
shared `.github/workflows/pages.yml` runs `pages/build`, and
`pages/finish-site.py` adds the labs bar (`pages/labs-bar.js`) whose home link is
this site. `pages/labs-bar.js`, `pages/finish-site.py` and the workflow are the
same in all six repositories; change them in all six.
