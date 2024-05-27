variable "DATABASE_PASSWORD" {
  description = "Password to database"
  sensitive   = true
}

variable "GOOGLE_CLIENT_ID" {
  description = "Google oauth2 client ID"
  sensitive   = true
}

variable "GOOGLE_CLIENT_SECRET" {
  description = "Google oauth2 client secret"
  sensitive   = true
}

variable "TOKEN_URL" {
  description = "Google oauth2 token URL"
  sensitive   = true
}

variable "GOOGLE_REDIRECT_URI" {
  description = "Google oauth2 redirect URI"
  sensitive   = true
}
