resource "google_cloud_run_service" "rag_api" {
  name     = "ragapi"
  location = "us-central1"
  template {
    spec {
      containers {
        image = "docker.io/azoz01/rag_api"
        ports {
          container_port = 8000
        }
        startup_probe {
          tcp_socket {
            port = 8000
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