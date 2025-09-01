module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = var.fluxter_name
  description   = "Manages tracking site's for raw etc data"
  handler       = "src.fluxter.handler.handle"
  runtime       = var.lambda_runtime

  create_package         = false
  local_existing_package = "${local.dist_path}src.fluxter${local.lambda_zip_suffix}"

  tags = {
    Name = var.fluxter_name
  }
}