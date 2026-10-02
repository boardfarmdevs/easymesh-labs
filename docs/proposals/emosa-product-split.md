# EMOSA's product apart from its lab, at the handover

**Status:** proposal, for the handover (alignment plan 8.6). The other components that
earned repositories of their own have them: the RF medium and the optimizer with its
room service.

## The test

A component earns its own repository when it has **one owner, one contract and more
than one consumer**, and when living inside a consumer makes it diverge or hides it.

## EMOSA: one repository, split product from lab at the handover

emosa-lab is EMOSA's own repository, so the question is a different one: should the C
and the Python be apart? **No.** They share one contract (the specification, the
schemas, the conformance vectors) and one test harness (the lab in a box runs either
implementation). Apart, the contract would have to live in a third place or be copied,
and the vectors would lose their oracle, the Python reference.

What does not fit the next team is the rest of emosa-lab: the evaluation and learning
material, the lab drivers, the experiments. The team that owns the C needs the product,
not the history.

**Proposal:** at the handover, carve `boardfarmdevs/emosa` out of emosa-lab: `spec/`,
`schemas/`, the vectors, `src/emosa/`, `c/`, the adapter kit, the tests and the lab in a
box. emosa-lab keeps the evaluation, learning and lab drivers and pins emosa like the
labs pin the medium. Not before: the contract still changes, and one repository keeps a
contract change and both implementations in one commit.

## Not proposed

- **The RDK Yocto layer and the RDK lab** (both meta-cmf-bananapi-vcpe): the images and
  the lab change together (a controller patch and the room that tests it), and both have
  one owner.
- **The controllers' backends** (RDK's em_cli helper, prplmesh-lab's controller-ui): each
  belongs to its stack; the page they serve is already one, in the medium.
