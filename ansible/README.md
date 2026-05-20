# Ansible Project Structure — Best Practices

A recommended directory layout for organizations getting started with Ansible, following Ansible's official best practices and community-standard conventions.

---

## Directory Structure

```
ansible/
├── ansible.cfg                  # Project-level config (overrides /etc/ansible/ansible.cfg)
├── requirements.yml             # Galaxy roles/collections to install
│
├── inventories/
│   ├── production/
│   │   ├── hosts.yml            # Production inventory (YAML preferred over INI)
│   │   ├── group_vars/
│   │   │   ├── all.yml          # Vars for every host
│   │   │   ├── webservers.yml   # Vars for the 'webservers' group
│   │   │   └── dbservers.yml
│   │   └── host_vars/
│   │       ├── web01.yml        # Vars specific to web01
│   │       └── db01.yml
│   └── staging/
│       ├── hosts.yml
│       ├── group_vars/
│       │   ├── all.yml
│       │   └── webservers.yml
│       └── host_vars/
│
├── playbooks/
│   ├── site.yml                 # Master playbook (imports all others)
│   ├── webservers.yml           # Playbook targeting webservers group
│   ├── dbservers.yml
│   └── adhoc/                   # One-off or utility playbooks
│       ├── reboot.yml
│       └── update_packages.yml
│
├── roles/
│   ├── common/                  # Applied to all hosts (base config, packages, etc.)
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── ntp.conf.j2
│   │   ├── files/
│   │   ├── vars/
│   │   │   └── main.yml         # Role-internal vars (high precedence, not for overriding)
│   │   ├── defaults/
│   │   │   └── main.yml         # Role defaults (lowest precedence, meant for overriding)
│   │   ├── meta/
│   │   │   └── main.yml         # Role dependencies, Galaxy metadata
│   │   └── README.md
│   ├── nginx/
│   └── postgresql/
│
├── collections/                 # Vendored Ansible collections (optional)
│   └── ansible_collections/
│
├── plugins/                     # Custom plugins (filter, lookup, callback, etc.)
│   ├── filter_plugins/
│   └── callback_plugins/
│
├── files/                       # Global static files (shared across roles/plays)
├── templates/                   # Global Jinja2 templates
│
└── vault/
    └── secrets.yml              # Ansible Vault encrypted secrets
```

---

## Key Decisions Explained

### Inventories — Keep Environments Separate

Keep `production/` and `staging/` as **separate inventory directories** rather than one big `hosts` file. This ensures you can never accidentally target production when you meant staging.

```bash
ansible-playbook -i inventories/production playbooks/site.yml
```

### `group_vars` and `host_vars` — Live Next to the Inventory

Placing `group_vars/` and `host_vars/` **inside each inventory directory** (not at the project root) means staging and production can have completely different variable values for the same group name. Ansible discovers them automatically when you point at that inventory directory.

### Variable Precedence

From lowest to highest priority:

| Priority | Source |
|---|---|
| 1 (lowest) | `role/defaults/main.yml` — safe defaults, meant to be overridden |
| 2 | `inventories/<env>/group_vars/all.yml` — global env-level values |
| 3 | `inventories/<env>/group_vars/<group>.yml` — group-specific values |
| 4 | `inventories/<env>/host_vars/<host>.yml` — host-specific overrides |
| 5 | `role/vars/main.yml` — role internals, rarely overridden |
| 6 (highest) | Extra vars (`-e key=val`) — always wins |

### `site.yml` as the Master Playbook

```yaml
# playbooks/site.yml
- import_playbook: webservers.yml
- import_playbook: dbservers.yml
```

This lets you run everything with one command or target individual playbooks during development:

```bash
# Run everything
ansible-playbook -i inventories/production playbooks/site.yml

# Run just one playbook
ansible-playbook -i inventories/staging playbooks/webservers.yml
```

### Roles vs. Playbooks

- **Roles** — reusable, parameterized units of work (nginx config, user management, etc.)
- **Playbooks** — orchestration; which roles/tasks run against which hosts in what order

Keep roles generic and environment-agnostic. Let `group_vars` and `host_vars` inject environment-specific values.

### `ansible.cfg` at the Project Root

Committing this file ensures every team member gets the same defaults automatically.

```ini
[defaults]
inventory           = inventories/production
roles_path          = roles
collections_paths   = collections
vault_password_file = ~/.ansible_vault_pass
retry_files_enabled = False

[ssh_connection]
pipelining = True   # Big performance boost
```

### `vault/secrets.yml` — Always Encrypt Secrets

Never store plaintext passwords, API keys, or certificates in your repo. Encrypt with:

```bash
ansible-vault encrypt vault/secrets.yml
```

Reference vault vars in your `group_vars` files and let Ansible merge them at runtime.

---

## `requirements.yml` — Declare External Dependencies

```yaml
collections:
  - name: community.general
    version: ">=8.0"
  - name: amazon.aws

roles:
  - name: geerlingguy.docker
    version: "7.0.0"
```

Install everything with:

```bash
ansible-galaxy install -r requirements.yml
ansible-galaxy collection install -r requirements.yml
```

---

## What to Avoid

| Anti-pattern | Why it hurts |
|---|---|
| One giant `hosts` file for all environments | Easy to accidentally target the wrong environment |
| Putting `group_vars/` at the project root | Variables bleed across inventories unintentionally |
| Hardcoding secrets in vars files | Security exposure in version control |
| Skipping roles for "small" projects | Playbooks grow fast; retrofitting roles later is painful |
| Using INI inventory format | YAML is more expressive and handles edge cases better |
