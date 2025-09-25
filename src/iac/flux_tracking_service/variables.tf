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

variable "region" {
  type    = string
}

locals {
  icos_data_url = "http://data.icos-cp.eu"
  icos_meta_url = "http://meta.icos-cp.eu"
}