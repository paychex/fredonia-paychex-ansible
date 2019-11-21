
# This Vault Config file initiates consul

storage "consul" {
    address     = "localhost:8500"
    path        = "vault"
}

listener "tcp" {
    address     = "localhost:8200"
    tls_disable = 1
}
