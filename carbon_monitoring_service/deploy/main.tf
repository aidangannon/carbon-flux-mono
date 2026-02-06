terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.0.0"
    }
  }

  backend "s3" {}
}

locals {
  name           = "carbon-monitoring"
  icos_data_url  = "http://data.icos-cp.eu"
  icos_meta_url  = "http://meta.icos-cp.eu"
}

provider "aws" {
  region = var.aws_region
}

variable "python_runtime" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "pandas_layer_arn" {
  type = string
}

variable "core_layer_arn" {
  type = string
}

variable "icos_username" {
  type = string
}

variable "icos_password" {
  type = string
}

resource "aws_s3_bucket" "blob" {
  bucket_prefix = "${local.name}-blob"
}

resource "aws_dynamodb_table" "db" {
  name         = "${local.name}-db"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "partition_key"
  range_key    = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "partition_key"
    type = "S"
  }

  tags = {
    Name = "${local.name}-db"
  }
}

module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${local.name}-get-latest-submissions"
  description   = "Gets latest submissions for monitored sites"
  handler       = "carbon_monitoring_service.src.entry_points.get_latest_submissions.handle"
  runtime       = var.python_runtime

  timeout = 30

  layers = [
    var.core_layer_arn
  ]

  create_package         = false
  local_existing_package = "../dist/carbon_monitoring_service.src.entry_points/get_latest_submissions_lambda.zip"

  attach_policy_statements      = true
  attach_cloudwatch_logs_policy = true
  policy_statements = {
    s3_access = {
      effect = "Allow"
      actions = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:PutObjectAcl"
      ]
      resources = ["${aws_s3_bucket.blob.arn}/*"]
    }
    dynamodb_access = {
      effect = "Allow"
      actions = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ]
      resources = [aws_dynamodb_table.db.arn]
    }
  }

  environment_variables = {
    ICOS_DATA_URL  = local.icos_data_url
    ICOS_META_URL  = local.icos_meta_url
    HOME           = "/tmp"
    DYNAMO_TABLE   = aws_dynamodb_table.db.name
    DYNAMO_REGION  = var.aws_region
  }

  tags = {
    Name = local.name
  }
}

module "lambda_hourly_trigger" {
  source     = "terraform-aws-modules/eventbridge/aws"
  create_bus = false
  rules = {
    hourly_lambda = {
      name                = "${local.name}-hourly-trigger"
      description         = "Trigger ${local.name} every hour"
      schedule_expression = "cron(0 */1 * * ? *)"
    }
  }
  targets = {
    hourly_lambda = [
      {
        name            = "lambda-target"
        arn             = module.lambda_function.lambda_function_arn
        dead_letter_arn = aws_sqs_queue.eventbridge-dlq.arn
        retry_policy = {
          maximum_retry_attempts       = 3
          maximum_event_age_in_seconds = 3600
        }
      }
    ]
  }
  tags = {
    Name = "${local.name}-hourly-trigger"
  }
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = module.lambda_hourly_trigger.eventbridge_rule_arns["hourly_lambda"]
}

resource "aws_sqs_queue" "eventbridge-dlq" {
  name                      = "${local.name}-eventbridge-hourly-trigger-dlq"
  message_retention_seconds = 1209600
}
