# Rust Toolchain

## Required Tools

| Tool | Purpose | Install | Invocation |
|------|---------|---------|------------|
| cargo-modules | Dep graph | `cargo install cargo-modules` | `cargo modules structure --package <crate>` |
| cargo-deps | Crate graph | `cargo install cargo-deps` | `cargo deps --no-transitive-deps` |
| clippy | Lints + complexity | ships with Rust | `cargo clippy --message-format json -- -W clippy::cognitive_complexity` |
| jscpd | Duplication | `npm i -g jscpd` | `jscpd --reporters json src` |
| cargo-geiger | Unsafe audit (optional) | `cargo install cargo-geiger` | `cargo geiger --output-format Json` |

## Minimum Versions

- Rust >=1.75 stable
- cargo-modules >=0.16

## Output Locations

`.rcc/aref-raw/{ts}-rs-<tool>.json`.

## Notes

- Workspace: iterate each member crate.
- Cyclic deps: rust compiler forbids at module level, but cross-crate cycles in workspace members should be flagged.
