terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "fluxter"
  description   = "Manages tracking site's for raw etc data"
  handler       = "src.fluxter.handler.handle"
  runtime       = "python3.11"

  create_package         = false
  local_existing_package = "../../dist/src.fluxter/lambda.zip"

  tags = {
    Name = "fluxter"
  }
}