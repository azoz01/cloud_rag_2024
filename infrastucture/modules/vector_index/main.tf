module "document_store" {
  source = "../bucket"
  name   = var.bucket_name
}

resource "google_vertex_ai_index" "vector_index" {
  display_name = var.vector_index_name
  region       = "us-central1"
  metadata {
    contents_delta_uri = "gs://${var.bucket_name}/${var.documents_directory}"
    config {
      dimensions                  = 100
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
  index_update_method = "BATCH_UPDATE"
  depends_on          = [module.document_store]
}

resource "google_vertex_ai_index_endpoint" "vector_index_endpoint" {
  display_name = "${var.vector_index_name}-endpoint"
  region       = "us-central1"
  depends_on   = [google_vertex_ai_index.vector_index]
}
