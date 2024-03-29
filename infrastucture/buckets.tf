resource "google_storage_bucket" "deployments" {
 name          = "deployments-cloudragmini2024"
 location      = "us-central1"
 storage_class = "STANDARD"
 force_destroy = true
}