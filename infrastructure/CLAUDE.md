# Infrastructure

No real resources are defined; both trees are skeletons awaiting the first deployable service.

- **Terraform:** provider-only config. `default_tags` stamps `Project`/`Environment`/`ManagedBy` onto
  every resource, so don't re-tag individually.
- **Ansible:** `site.yml` is a connectivity-check playbook. `ansible.cfg` hardcodes
  `inventory = inventory/hosts`, so run `ansible-playbook` from `infrastructure/ansible/` and copy
  `inventory/hosts.example` → `inventory/hosts` first (the real inventory is gitignored).
