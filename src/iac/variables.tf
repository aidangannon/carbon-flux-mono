variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

variable "fluxter_name" {
  type    = string
  default = "fluxter"
}

variable "lambda_runtime" {
  type    = string
  default = "python3.11"
}

locals {
  dist_path = "../../dist/"
  lambda_zip_suffix = "/lambda.zip"
}
