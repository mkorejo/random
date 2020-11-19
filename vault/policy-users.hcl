# List, create, and update KV secrets
path "secret/*" {
  capabilities = ["create", "update", "list"]
}

path "databases/*" {
  capabilities = ["create", "update", "list"]
}

# List existing secret engines
path "sys/mounts" {
  capabilities = ["read"]
}