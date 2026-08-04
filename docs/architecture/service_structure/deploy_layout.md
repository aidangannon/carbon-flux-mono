# `deploy/` layout

[← Service structure index](./index.md)

- Terraform for the service lives in [`deploy/`](../../../carbon_monitoring_service/deploy)
- Deployed via `pants experimental-deploy` in CI (see [`build_system.md`](../build_system.md)), which runs `terraform apply -auto-approve` only on push to trunk and only when `pants package` produced artifacts
