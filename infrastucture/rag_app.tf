resource "google_cloud_run_service" "rag_app" {
  name     = "ragapp"
  location = "us-central1"
  template {
    spec {
      containers {
        image = "docker.io/azoz01/rag_app"
        ports {
          container_port = 8001
        }
        startup_probe {
          tcp_socket {
            port = 8001
          }
        }
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
  metadata {
    annotations = {
      "run.googleapis.com/ingress" = "all"
    }
  }
  depends_on = [ google_project_service.run_api ]
}