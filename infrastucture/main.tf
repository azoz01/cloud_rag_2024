provider "google" {
  project = "cloudragmini20242"
  credentials = "${file("../credentials/key.json")}"
  region  = "europe-west10"
  zone    = "europe-west10-c"
}
