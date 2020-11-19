# Manage authentication methods broadly across Vault
path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Create, update, and delete authentication methods
path "sys/auth/*" {
  capabilities = ["create", "update", "delete", "sudo"]
}

# List authentication methods
path "sys/auth" {
  capabilities = ["read"]
}

# List existing policies
path "sys/policies/acl" {
  capabilities = ["list"]
}

# Create and manage ACL policies
path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# List, create, update, and delete KV secrets
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "databases/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Manage secret engines
path "sys/mounts/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# List existing secret engines
path "sys/mounts" {
  capabilities = ["read"]
}

# Read health checks
path "sys/health" {
  capabilities = ["read", "sudo"]
}

# JWT settings
path "jwt/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}