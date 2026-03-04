# Agent Knowledge Layer

Single GitHub repository for multi-agent shared knowledge storage.

## Layout

- `private/<agent>/`: per-agent working knowledge (high-frequency edits)
- `shared/`: reviewed public knowledge (merge via PR)
- `meta/`: registry, changelog, sync metadata
- `templates/`: note templates and contribution templates

## Branch model

- `main`: stable shared knowledge
- `agent/<name>`: each agent working branch
- Promote knowledge via PR from `agent/<name>` to `main`

## Core rule

Do not edit `main` directly for shared documents. Use PR.
