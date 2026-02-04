locals {
  python_runtime = "python3.13"
  aws_region = "eu-west-2"
}

variable "icos_username" {
  type    = string
}

variable "icos_password" {
  type    = string
}
