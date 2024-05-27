provider "google" {
  project     = "cloudragmini20242"
  credentials = file("../credentials/key.json")
  region      = "europe-west10"
  zone        = "europe-west10-c"
}

module "gcp_apis" {
  source = "./modules/gcp_apis"
}

module "database" {
  source                 = "./modules/database"
  database_name          = "historycloudragmini2024"
  database_instance      = "db-f1-micro"
  database_user_name     = "rag_user"
  database_user_password = var.DATABASE_PASSWORD
  depends_on             = [module.gcp_apis]
}

module "vector_index" {
  source              = "./modules/vector_index"
  bucket_name         = "document-store-cloudragmini2024"
  vector_index_name   = "vector-index-cloudragmini2024"
  documents_directory = "contents"
  depends_on          = [module.gcp_apis]
}

module "rag_api" {
  source           = "./modules/run_app"
  application_name = "ragapi"
  location         = "us-central1"
  docker_img       = "docker.io/azoz01/rag_api:0.0.20"
  port             = 8000
  environment = {
    "DATABASE_IP"           = module.database.database_ip,
    "DATABASE_USER"         = module.database.user,
    "DATABASE_PASSWORD"     = module.database.password,
    "PROJECT_ID"            = "cloudragmini20242",
    "VECTOR_INDEX_REGION"   = module.vector_index.vector_index_region,
    "VECTOR_INDEX_BUCKET"   = module.vector_index.bucket_name,
    "VECTOR_INDEX_ID"       = module.vector_index.vector_index_id,
    "ENDPOINT_ID"           = module.vector_index.vector_index_endpoint_id
    "GOOGLE_CLIENT_ID"      = var.GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET"  = var.GOOGLE_CLIENT_SECRET,
    "TOKEN_URL"             = var.TOKEN_URL,
  }
  depends_on = [
    module.gcp_apis,
    module.database,
    module.vector_index
  ]
}

module "rag_app" {
  source           = "./modules/run_app"
  application_name = "ragapp"
  location         = "us-central1"
  docker_img       = "docker.io/azoz01/rag_app:0.0.4"
  port             = 8001
  environment = {
    "API_URL" = module.rag_api.url
  }
  depends_on = [
    module.rag_api,
    module.gcp_apis
  ]
}
