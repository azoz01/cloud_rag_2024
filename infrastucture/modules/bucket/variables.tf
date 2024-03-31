variable "name" {
  description = "Name of the bucket"
  type        = string
}

variable "force_destroy" {
  description = "Whether to force the destroy"
  type        = bool
  default     = false
}
