variable "database_name" {
  description = "Name of database instance"
  type        = string
}

variable "database_instance" {
  description = "Instance type of database"
  type        = string
}

variable "database_user_name" {
  description = "Name of database user"
  type        = string
}

variable "database_user_password" {
  description = "Password of database user"
  type        = string
}

output "database_ip" {
  description = "IP of the database"
  value       = google_sql_database_instance.users_history_db.public_ip_address
}

output "user" {
  description = "Username of database user"
  value       = google_sql_user.rag_user.name
}

output "password" {
  description = "Password of database user"
  value       = google_sql_user.rag_user.password
}
