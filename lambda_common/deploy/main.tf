variable "python_runtime" {
  type = string
}

variable "aws_region" {
  type = string
}

locals {
  file_name = "../../dist/lambda_common/common_layer.zip"
}

resource "aws_lambda_layer_version" "core_layer" {
  filename            = local.file_name
  layer_name          = "common"
  compatible_runtimes = [var.python_runtime]

  source_code_hash = filebase64sha256(local.file_name)
}
