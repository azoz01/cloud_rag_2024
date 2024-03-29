resource "google_storage_bucket" "document_store" {
    name          = "document-store-cloudragmini2024"
    location      = "us-central1"
    storage_class = "STANDARD"
}

resource "google_vertex_ai_index" "vector_index" {
  display_name = "vector-index-cloudragmini2024"
  region   = "us-central1"
  metadata {
    contents_delta_uri = "gs://${google_storage_bucket.document_store.name}/contents"
    config {
      dimensions = 100
      approximate_neighbors_count = 10
      shard_size = "SHARD_SIZE_SMALL"
      algorithm_config {
        tree_ah_config {
          leaf_node_embedding_count = 500
          leaf_nodes_to_search_percent = 7
        }
      }

    }
  }
  index_update_method = "BATCH_UPDATE"
}