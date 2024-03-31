resource "google_storage_bucket" "bucket" {
  name          = var.name
  location      = "us-central1"
  storage_class = "STANDARD"
  force_destroy = var.force_destroy
}
