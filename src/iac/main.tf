module "fluxter" {
  source          = "./fluxter"
  python_runtime  = var.python_runtime
  name            = "fluxter"
  icos_username   = var.icos_username
  icos_password   = var.icos_password

  core_layer_arn  = aws_lambda_layer_version.core_layer.arn
}