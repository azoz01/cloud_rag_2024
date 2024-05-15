module "document_store" {
  source        = "../bucket"
  name          = var.bucket_name
  force_destroy = true
}

resource "google_vertex_ai_index" "vector_index" {
  display_name = var.vector_index_name
  region       = "us-central1"
  metadata {
    contents_delta_uri = "gs://${var.bucket_name}/${var.documents_directory}"
    config {
      dimensions                  = 768
      approximate_neighbors_count = 10
      shard_size                  = "SHARD_SIZE_SMALL"
      algorithm_config {
        tree_ah_config {
          leaf_node_embedding_count    = 500
          leaf_nodes_to_search_percent = 7
        }
      }

    }
  }
  index_update_method = "STREAM_UPDATE"
  depends_on          = [module.document_store]
}

resource "google_vertex_ai_index_endpoint" "vector_index_endpoint" {
  display_name = "${var.vector_index_name}-endpoint"
  region       = "us-central1"
  depends_on   = [google_vertex_ai_index.vector_index]
}

resource "null_resource" "deploy_google_vertex_ai_index_endpoint" {
  provisioner "local-exec" {
    command     = <<-EOT
        gcloud ai index-endpoints deploy-index ${google_vertex_ai_index_endpoint.vector_index_endpoint.name} \
          --deployed-index-id=vectorindexendpointcloudragmini \
          --display-name=${var.vector_index_name} \
          --index=${google_vertex_ai_index.vector_index.name} \
          --machine-type="e2-standard-2" \
          --min-replica-count=1 \
          --max-replica-count=1 \
          --region=us-central1 \
          --project=cloudragmini20242
    EOT
  }
  depends_on = [google_vertex_ai_index_endpoint.vector_index_endpoint, google_vertex_ai_index.vector_index]

}