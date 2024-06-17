provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}


resource "google_artifact_registry_repository" "repository" {
  repository_id = var.resource_name
  location      = var.location != null ? var.location : var.gcp_region
  format        = var.format
  # TODO: add additional configuration
}


output "gcp_id" {
  value = google_artifact_registry_repository.repository.id
}
