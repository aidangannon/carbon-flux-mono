variable "name" {
  type    = string
}

variable "python_runtime" {
  type    = string
}

variable "pandas_layer_arn" {
  type    = string
}

variable "core_layer_arn" {
  type    = string
}

variable "icos_username" {
  type    = string
}

variable "icos_password" {
  type    = string
}

locals {
  icos_data_url = "https://data.icos-cp.eu"
  icos_meta_url = "https://meta.icos-cp.eu"
}