variable "bucket_name" {
  description = "Name of the document store bucket"
  type        = string
}

variable "vector_index_name" {
  description = "Name of the vector index"
  type        = string
}

variable "documents_directory" {
  description = "Directory of the documents in the bucket"
  type        = string
}

output "vector_index_region" {
  description = "Region of vector index"
  value       = google_vertex_ai_index.vector_index.region
}

output "vector_index_id" {
  description = "ID of vector index"
  value       = google_vertex_ai_index.vector_index.name
}

output "vector_index_endpoint_id" {
  description = "ID of vector index endpoint"
  value       = google_vertex_ai_index_endpoint.vector_index_endpoint.name
}

output "bucket_name" {
  description = "Name of the document store bucket"
  value       = var.bucket_name
}

