# More components in repositories of their own

**Status:** Section 2 done on 30 September: [easymesh-optimizer](https://github.com/boardfarmdevs/easymesh-optimizer),
pinned by both labs and requalified in both (plan 6.5). Section 3 done the same day:
the room service is easymesh-optimizer's second package (plan 6.6). Section 4 waits
for the handover.

**Prepared:** 30 September 2026, from the user's question of the same day (should
the optimizer, or EMOSA's C and Python, be in repositories of their own?), after
the posters (`site/posters/`) mapped where every component lives.

## 1. The test

A component earns its own repository when it has **one owner, one contract and
more than one consumer**, and when living inside a consumer makes it diverge or
hides it. easymesh-medium passed this test on 29 September: two diverging copies
in two labs, one contract (the room language, the wmediumd patch series), two
consumers. It is now one repository that both labs pin and requalify on.

## 2. The optimizer: yes (plan 6.5, done)

Measured on 30 September between meta-cmf-bananapi-vcpe `gen/optimizer` and
prplmesh-lab `optimizer`:

| | Files |
| --- | --- |
| identical | 61 |
| differ | 23 (3 944 changed lines) |
| RDK only | 5 |
| prplMesh only | 9 |

The differences sit where each stack is read and driven: `observer.py`,
`candidates.py`, `streaming.py`, `traffic.py`, `cli.py` and their tests. The
policy itself (planners, load policy, verifier, recorder) is shared. That is the
shape the medium had: a common core with stack-specific parts, which
easymesh-medium solved with one module naming the stacks' differences
(`configurator/wmdcfg/stacks.py`).

The optimizer is also the reason for the first goal (optimizer development in a
rich virtual lab), and today a newcomer cannot find it: it is a subdirectory of a
Yocto layer and of a lab.

**Proposal:** `boardfarmdevs/easymesh-optimizer`, holding the optimizer package,
its scenarios, policy configurations and tests, with one adapter per stack (RDK
through em_cli, prplMesh through NBAPI), pinned by both labs as a submodule like
the medium, and requalified in both. The physical lab's `optimizer.py` (88 lines,
a teaching tool on one real agent) stays where it is.

## 3. The room service: with the optimizer (plan 6.6, done)

The room service (`room_demo`, the live room on port 8891) hosts the optimizer
and drives the lab while a room plays. 22 files are identical, 28 differ (1 841
lines), 19 are RDK only (pods, the wired extender, EMOSA's backhaul moves) and 5
prplMesh only. It is the optimizer's runtime and has no consumer without it.

**Proposal:** in easymesh-optimizer too, as its second package, with the same
per-stack adapters. The viewer stays in easymesh-medium (it plays the medium's
rooms, and the public sandbox needs no optimizer).

## 4. EMOSA: already its own; split product from lab at the handover

emosa-lab is EMOSA's own repository today, so the question is a different one:
should the C and the Python be apart? **No.** They share one contract (the
specification, the schemas, the conformance vectors) and one test harness (the
lab in a box runs either implementation). Apart, the contract would have to live
in a third place or be copied, and the vectors would lose their oracle, the
Python reference.

What does not fit the next team is the rest of emosa-lab: about 4 800 files of
evidence, evaluation and learning material, the lab drivers, the experiments.
The team that owns the C needs the product, not the history.

**Proposal:** at the handover (plan 8.6), carve `boardfarmdevs/emosa` out of
emosa-lab: `spec/`, `schemas/`, the vectors, `src/emosa/`, `c/`, the adapter kit,
the tests and the lab in a box. emosa-lab keeps the evidence, evaluation,
learning and lab drivers and pins emosa like the labs pin the medium. Not
before: the contract still changes (the admission rule was added on
30 September), and one repository keeps a contract change and both
implementations in one commit.

## 5. Not proposed

- **The RDK Yocto layer and the RDK lab** (both meta-cmf-bananapi-vcpe): the images
  and the lab change together (a controller patch and the room that tests it), and
  both have one owner.
- **The controllers' dashboards** (em_cli in RDK, `controller-ui` in prplmesh-lab):
  each belongs to its stack.
- **The room builder**: already its own repository.

## 6. Order

1. easymesh-optimizer (plan 6.5): measure, merge the copies around per-stack
   adapters, both labs pin it, requalify both (their room suites), as phase 6.
2. emosa out of emosa-lab: at the handover, plan 8.6.
