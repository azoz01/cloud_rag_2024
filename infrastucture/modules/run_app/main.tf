resource "google_cloud_run_service" "app" {
  name     = var.application_name
  location = var.location
  template {
    spec {
      containers {
        image = var.docker_img
        ports {
          container_port = var.port
        }
        startup_probe {
          tcp_socket {
            port = var.port
          }
        }
        dynamic "env" {
          for_each = var.environment
          content {
            name  = env.key
            value = env.value
          }
        }
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.app.location
  project     = google_cloud_run_service.app.project
  service     = google_cloud_run_service.app.name
  policy_data = data.google_iam_policy.noauth.policy_data
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}
