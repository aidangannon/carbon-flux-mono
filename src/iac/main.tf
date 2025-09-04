module "fluxter" {
  source          = "./fluxter"
  python_runtime  = var.python_runtime
  name            = "fluxter"

  core_layer_arn  = aws_lambda_layer_version.core_layer.arn
}