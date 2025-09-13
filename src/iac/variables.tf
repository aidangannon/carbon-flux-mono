locals {
  python_runtime = "python3.11",
  aws_region = "eu-west-2"
}

variable "icos_username" {
  type    = string
}

variable "icos_password" {
  type    = string
}