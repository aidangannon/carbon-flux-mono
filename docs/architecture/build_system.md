# BUILD file structure

[← Architecture index](./index.md)

- With pants we use `BUILD` files to determine which files make up a dependency in the source

## Examples
- [`carbon_monitoring_service/src/BUILD`](../../carbon_monitoring_service/src/BUILD): covers the service's source files, excluding `contracts.py`, which gets its own build artifact in the same `BUILD` file since it's a separate dependency. This means both the producer and consumer of the contracts can rely on this dependency through pants, rather than through a versioned lib, which causes a bump cycle.
- [`carbon_monitoring_service/src/entry_points/BUILD`](../../carbon_monitoring_service/src/entry_points/BUILD): contains all the definitions for the lambda functions, which need to be built separately as they are separate packaged lambdas.
    - It runs through `python_aws_lambda_function`, which is a pants specific way for building zippable lambda distributable artifacts.

## Coding standard for defining build files
- Define global dependency in: [`pyproject.toml`](../../pyproject.toml)
- Reference that dependency in the code, then run `pants export`, venv should be symlinked: look at [`pants.toml`](../../pants.toml)
- You shouldn't have to define each dependency in the BUILD file, pants will automatically resolve dependencies for us

## Global pants config
- Global config for pants is defined in [`pants.toml`](../../pants.toml)

## CI/CD: only build/test what changed
- Commands are defined in [`.github/workflows/cicd.yml`](../../.github/workflows/cicd.yml)
- `--changed-since=HEAD~1 --changed-dependents=transitive` is passed to all pants commands, so only what changed since last build is run
- Meaning we don't build/run tests for bits that don't need it
