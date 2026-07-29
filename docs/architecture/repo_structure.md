# Mono repo structure

- It's a mono repo. Each folder at repo root is a 'thing': either a **service** (deployable unit) or a **shared library** consumed by services.

## Examples of things currently at root
- [`carbon_monitoring_service`](../../carbon_monitoring_service): a service (see layout below)
- [`lambda_common`](../../lambda_common): shared library, packaged as a Lambda layer (see [`lambda_common/BUILD`](../../lambda_common/BUILD)), consumed by services rather than versioned/published
- [`pyight_bdd`](../../pyight_bdd): shared test tooling

## Service layout
- A service (e.g. [`carbon_monitoring_service`](../../carbon_monitoring_service)) is a deployable unit bound to a schema
- `src`: source code, its own module within the service
- `tests`: test suite, its own module that references `src`
- `deploy`: Terraform for that service
- A service describes a bunch of lambdas/handlers/endpoints. Each lambda is a separate cloud-native thing, but together they serve related business functions and are bound to 1 schema.

## Build system
- [Pants](https://www.pantsbuild.org/) ([`pants.toml`](../../pants.toml), `BUILD` files per directory, e.g. [`/BUILD`](../../BUILD)) drives builds, lint, typecheck and test
- It's what makes "only build/test/deploy what changed" possible in a repo this shape
- See [`build_system.md`](./build_system.md)

## Why mono repo (for a project this size)
- Simple & collaborative at small scale
- Everything in one place: easy to understand the whole
- Shared deps (e.g. [`lambda_common`](../../lambda_common)) co-exist unversioned, no publish/bump cycle
- Standards enforced repo-wide, and checked out alongside the code that uses them (see [`docs/index.md`](../index.md), [`docs/coding_standards`](../coding_standards) (empty, TODO), [`docs/tooling`](../tooling) (empty, TODO))

## Where it breaks down
- Needs a build system (Pants) to scope builds/tests/deploys to only the things that changed
- Needs homogeneity: CI/CD pipeline is shared across all things
- Gets harder as things diverge from each other
- Past ~100 services, needs partial checkouts and/or custom git tooling
