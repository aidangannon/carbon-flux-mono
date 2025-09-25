module "flux_tracking_service" {
  source            = "./flux_tracking_service"
  python_runtime    = local.python_runtime
  name              = "flux-tracking"

  icos_username     = var.icos_username
  icos_password     = var.icos_password

  core_layer_arn    = aws_lambda_layer_version.core_layer.arn
  pandas_layer_arn  = local.pandas_layer_arn

  region            = local.aws_region
}