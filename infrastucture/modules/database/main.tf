resource "google_sql_database_instance" "users_history_db" {
  name                = var.database_name
  database_version    = "POSTGRES_14"
  deletion_protection = false
  settings {
    tier = var.database_instance
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "allow_all"
        value = "0.0.0.0/0"
      }
    }
  }
}

resource "google_sql_user" "rag_user" {
  name       = var.database_user_name
  instance   = google_sql_database_instance.users_history_db.name
  password   = var.database_user_password
  depends_on = [google_sql_database_instance.users_history_db]
}

resource "null_resource" "setup_users_history_db" {
  provisioner "local-exec" {
    command     = <<-EOT
        sh ./scripts/db_setup/setup.sh \
            ${google_sql_database_instance.users_history_db.public_ip_address} \
            ${var.database_user_name} \
            ${var.database_user_password}
    EOT
    working_dir = "modules/database"
  }
  depends_on = [google_sql_database_instance.users_history_db, google_sql_user.rag_user]

}
