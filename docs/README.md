# The umbrella's documents

[Repository](../README.md) · [Site](https://mesh.vcpe.dev/)

| Document | Kind | What it covers |
| --- | --- | --- |
| [Lab configurations](reference/lab-configurations.md) | reference | the six VM lab configurations, the VMs that run now and the hosts |
| [Alignment plan](project/alignment-plan.md) | project | the plan that aligns the labs, up to EMOSA in C in the RDK gateway image, and its status |
| [Open work](project/open-work.md) | project | the priorities both optimizer labs carry forward, with owners and completion evidence |
| [Project assessment](project/assessment.md) | project | the whole project against its goals (2 October 2026): what was fixed, what is recommended for later, what to stop |
| [Proposals register](project/proposals.md) | project | every proposal of the labs, wherever it is kept, with its decision: chosen, open, parked or retired |
| [Labs as a service](proposals/labs-as-a-service.md) | proposal | the labs for remote optimizer developers, through an API; parked |
| [EMOSA's product apart from its lab](proposals/emosa-product-split.md) | proposal | carving the EMOSA product out of emosa-lab at the handover |
| [Faster, cheaper labs](proposals/faster-labs.md) | proposal | where build and requalification time goes, what is already precooked, and what to change: updates in place, requalifying what a change affects, precooked images and an artifact store keyed by inputs |

Two subjects have their own repositories and documents since 2 October 2026: the labs'
Wi-Fi clients ([easymesh-clients](https://vcpe.dev/easymesh-clients/): what each lab's
clients are, the proposal for more capable clients, and the client models, which moved
there from here as a proposal and were built and checked on a bench there on 3 October) and
remote access ([easymesh-remote](https://vcpe.dev/easymesh-remote/):
the gateway, its setup guide, what each lab publishes, and the proposal for remote labs,
which the labs as a service proposal above stands on). The proposals of every repository
are listed, with their decisions, in the [proposals register](project/proposals.md).

Every project of the labs keeps its documents the same way: `docs/README.md` indexes them,
and they are grouped by kind: `concepts/` (how something works), `guides/` (how to do
something), `reference/` (what exactly something is), `project/` (plans and decisions),
`records/` (what happened, dated) and `proposals/` (not implemented).
