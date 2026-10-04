# Project assessment

[Documents](../README.md)

**Kind:** project. An assessment of the whole project against its goals, made on
2 October 2026, and what came of it. The status column is kept as items are done.

**The question:** shortcomings, things obsolete, and opportunities for alignment,
accessibility and usability, without expanding further. The time and cost of building and
requalifying the labs are understood and outside this assessment.

## 1. The verdict

The project is close to a good balance. The core holds: the RF medium, the optimizer and
EMOSA exist once each, both optimizer labs pin the shared parts and are rebuilt from main,
the shared components have CI, and the documentation rules are enforced everywhere. The
weaknesses were not missing features. They were things built but not switched on, too many
overlapping proposals, a few maintenance costs repeated in every repository, and two gaps
that limit what an optimizer result proves.

## 2. Findings and what was done

Quick fixes first (Q), then the findings (1 to 8).

| # | Finding | Status | What was done, or what remains |
| --- | --- | --- | --- |
| Q1 | The umbrella's repositories table linked the private resources repository: a 404 for visitors | **done** (2 Oct) | it links the resources' site |
| Q2 | The alignment plan's hosts table named a VM deleted that day | **done** (2 Oct) | it names configurations; the VMs are in the lab configurations |
| Q3 | The remote access pages repeated VM names and the host ports of one build | **done** (2 Oct) | configuration names (`rdk-MMDD`), default ports, the lab configurations for the rest |
| Q4 | The room builder's parity test ran only by hand | **done** (2 Oct) | item 7 |
| Q5 | No list of the proposals and their state | **done** (2 Oct) | [the proposals register](proposals.md) |
| 1 | **Built but not in use.** The remote access gateway is installed on no host, so nobody off the lab network can use a lab | open | R1 |
| 2 | **What an optimizer result proves.** All 100 clients are the same obedient client; rooms give pass or fail but no numbers to compare two algorithms by | open | R2, R3 (R3's client models are built and checked on a bench, 3 Oct; no room uses them yet) |
| 3 | **Too many open proposals.** Eleven in six repositories; five overlapping on optimizer work from outside, three on a Data Elements view, two disagreeing on the route | **done** (2 Oct) | the register gives each a status. The rooms plan is retired (two of its ideas parked); labs as a service is parked as the API alternative; plugins are the chosen route; client models moved to easymesh-clients; the Data Elements view has one owner |
| 4 | **The same facts kept in many places.** The page tooling copied into ten repositories (adding a repository took ten commits each time); VM names repeated where the rule says they live in one place | **done** (2 Oct) | one shared Pages workflow (`.github/workflows/labs-pages.yml` here) that the ten repositories with a site call; the documentation check, the finishing step and the labs bar exist once, here, and the bar is served from <https://mesh.vcpe.dev/labs-bar.js>, so a change to it is one commit. The lab configurations' own two tables disagreed (the configurations table named four deleted VMs); VM names are now only in its hosts table. Remaining by design: each lab's state section and the dated labs poster name their VMs |
| 5 | **Weight.** emosa-lab checked out 825 MB, 816 MB of it evidence under `docs/records`, single files up to 42 MB | **done** (2 Oct) | the 117 raw captures and recordings over 256 KB (pcap, jsonl: 547 MB) live in emosa-lab's release `evidence-2026-10-02` (18.5 MB compressed). `docs/records/evidence/external.json` lists them with sizes and SHA-256; `scripts/fetch-evidence.py` puts them back, checked; CI fetches first; the tests stop with that instruction when they are missing. The checkout is 278 MB, the largest file 10 MB. Remaining: R9 |
| 6 | **Breakage found late.** The labs' Python and Node tests that need no VM did not run in CI | **done** (2 Oct, by the labs) | both labs run their suites' static tiers in CI on every push (RDK: the static stage, 56 checks; prplMesh: static and webui, 58). The OpenSync lab still has no tests ([open work](open-work.md)) |
| 7 | **The room builder can drift** from the medium's compiler it ports | **done** (2 Oct) | its CI checks byte parity against the medium commit the umbrella's manifest pins, on every push (73 tests, 3 of them parity) |
| 8 | **The oldest running lab** predated the splits | **resolved** (2 Oct) | rebuilt with every lab on 2 October; see the lab configurations |

## 3. Recommendations kept for later

None of these is started. Each names a first step that is small.

| # | Recommendation | Why | First step |
| --- | --- | --- | --- |
| R1 | **Switch the gateway on** for one lab | the remote access built in September is used by nobody | publish the RDK lab with EMOSA privately on rev120, which already runs Tailscale; two accounts; the checks in easymesh-remote's setup guide |
| R2 | **A scorecard** for optimizer runs: time to converge, steers, failures, oscillations, per room | goal 1 is optimizer development, and better needs a number; plugins are only useful with one | compute it from the events the room already emits; the workbench proposal's section 13 has the design |
| R3 | **Clients that behave like devices** | an optimizer tested only against obedient clients has met the easiest case | started 3 Oct: requirements, design and a bench test plan in easymesh-clients. Built the same day on a bench, in easymesh-clients: wpa_supplicant 2.12 with three patches, 14 models, every conformance test passed in 441 runs. Next: one lab takes the build (2.12 as today's client, with that lab's suite), then one model by hand in a room |
| R4 | **A standing lab**: one lab always up and reachable privately, refreshed at each requalification | the labs then work as a service for the team, not as a build | follows R1 |
| R5 | **Start paths by role** on the landing page: an optimizer developer, an EMOSA integrator, a newcomer | the sites are long (the optimizer's page is about 30 minutes) | three short lists of links, no new pages |
| R6 | **One set of lab commands**: a thin `lab` command with the same verbs in every lab (build, up, status, suite, room) | each lab names its scripts differently; the remote directory would call the same verbs | the verbs and their mapping to each lab's scripts, written down first |
| R7 | **Names**: keep using the display names (the bar already does) | `easymesh-labs` and `easymesh-lab` differ by one letter; renaming breaks every URL | nothing to do |
| R8 | **The public posters' LAN addresses** | outsiders cannot use them and they go stale | decide at the next poster update; low priority |
| R9 | **emosa-lab's remaining records** (269 MB: JSON samples 138 MB, JUnit XML 115 MB) | the same weight, smaller | the XML results are linked from 15 documents; move them with those links rewritten, as for the raw files |
| R10 | **The RDK lab's copy of the gateway** (`gen/remote-access`, its tests, its manual) | two copies since easymesh-remote took it | remove it when easymesh-remote's gateway is the one installed (R1) |
| R11 | **The labs block** in every README names neither the clients, remote access nor the resources | the block is the labs' shared introduction | decide whether it should; a change touches every repository |

## 4. What to stop

- **Adding proposals** beside the register: a subject with a proposal extends it.
- **Adding repositories.** Twelve is enough. The clients and remote access stay what they
  are (documents, and the gateway) until a lab needs more from them.
- **Writing the same fact in several places.** VM names live in the lab configurations;
  shared tooling lives here.
