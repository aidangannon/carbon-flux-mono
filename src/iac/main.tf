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

  function_name = "blah"
  description   = "blah"
  handler       = "todo"
  runtime       = "python3.11"
  memory_size   = 512

  create_package         = false
  local_existing_package = "../../dist/src.blahblahblah.zip"

  tags = {
    Name = "sitetracking"
  }
}