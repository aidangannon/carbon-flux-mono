resource "aws_lambda_layer_version" "core_layer" {
  filename            = local.file_name
  layer_name          = "common"
  compatible_runtimes = [var.python_runtime]

  source_code_hash = filebase64sha256(local.file_name)
}

locals {
  file_name = "../../dist/src.common/layer.zip"
}

locals {
  # find latest version at https://api.klayers.cloud/api/v2/p3.11/layers/latest/eu-west-2
  pandas_layer_arn = "arn:aws:lambda:${var.aws_region}:770693421928:layer:Klayers-p311-pandas:22"
}