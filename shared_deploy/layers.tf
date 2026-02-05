resource "aws_lambda_layer_version" "core_layer" {
  filename            = local.file_name
  layer_name          = "common"
  compatible_runtimes = [local.python_runtime]

  source_code_hash = filebase64sha256(local.file_name)
}

locals {
  file_name = " ../dist/lambda_common/common_layer.zip"
}

locals {
  klayers_runtime = "p312"
}

locals {
  # find latest version at https://api.klayers.cloud/api/v2/p3.12/layers/latest/eu-west-2
  pandas_layer_arn = "arn:aws:lambda:${local.aws_region}:770693421928:layer:Klayers-${local.klayers_runtime}-pandas:22"
  numpy_layer_arn = "arn:aws:lambda:${local.aws_region}:770693421928:layer:Klayers-${local.klayers_runtime}-numpy:14"
}
