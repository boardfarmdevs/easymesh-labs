# The umbrella's documents

[Repository](../README.md) · [Site](https://mesh.vcpe.dev/)

| Document | Kind | What it covers |
| --- | --- | --- |
| [Lab configurations](reference/lab-configurations.md) | reference | the six VM lab configurations, the VMs that run now and the hosts |
| [Alignment plan](project/alignment-plan.md) | project | the plan that aligns the labs, up to EMOSA in C in the RDK gateway image, and its status |
| [Open work](project/open-work.md) | project | the priorities both optimizer labs carry forward, with owners and completion evidence |
| [Client models](proposals/client-models.md) | proposal | clients that behave like different kinds of real devices |
| [Labs as a service](proposals/labs-as-a-service.md) | proposal | the labs for remote optimizer developers |
| [EMOSA's product apart from its lab](proposals/emosa-product-split.md) | proposal | carving the EMOSA product out of emosa-lab at the handover |

Two subjects have their own repositories and documents since 2 October 2026: the labs'
Wi-Fi clients ([easymesh-clients](https://vcpe.dev/easymesh-clients/): what each lab's
clients are, and the proposal for more capable clients, which builds on the client models
proposal above) and remote access ([easymesh-remote](https://vcpe.dev/easymesh-remote/):
the gateway, its setup guide, what each lab publishes, and the proposal for remote labs,
which the labs as a service proposal above stands on).

Every project of the labs keeps its documents the same way: `docs/README.md` indexes them,
and they are grouped by kind: `concepts/` (how something works), `guides/` (how to do
something), `reference/` (what exactly something is), `project/` (plans and decisions),
`records/` (what happened, dated) and `proposals/` (not implemented).
