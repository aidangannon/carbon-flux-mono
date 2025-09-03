module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = var.fluxter_name
  description   = "Manages tracking site's for raw etc data"
  handler       = "src.fluxter.handler.handle"
  runtime       = var.lambda_runtime

  create_package         = false
  local_existing_package = "${local.dist_path}src.fluxter${local.lambda_zip_suffix}"

  attach_policy_statements = true
  policy_statements = {
    s3_access = {
      effect = "Allow"
      actions = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:PutObjectAcl"
      ]
      resources = ["${aws_s3_bucket.data_bucket.arn}/*"]
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
      resources = [aws_dynamodb_table.fluxter_table.arn]
    }
  }

  tags = {
    Name = var.fluxter_name
  }
}

resource "aws_s3_bucket" "data_bucket" {
  bucket_prefix = "${var.fluxter_name}-blob"
}

resource "aws_dynamodb_table" "fluxter_table" {
  name           = "${var.fluxter_name}-db"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "partition_key"
  range_key      = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "partition_key"
    type = "S"
  }

  tags = {
    Name = "${var.fluxter_name}-db"
  }
}

module "lambda_hourly_trigger" {
    source = "terraform-aws-modules/eventbridge/aws"

    create_bus = false

    rules = {
      hourly_lambda = {
        name                = "${var.fluxter_name}-hourly-trigger"
        description         = "Trigger ${var.fluxter_name} every hour"
        schedule_expression = "cron(0 */1 * * ? *)"
      }
    }

    targets = {
      hourly_lambda = [
        {
          name = "lambda-target"
          arn  = module.lambda_function.lambda_function_arn
          dead_letter_arn = aws_sqs_queue.dlq.arn
          retry_policy = {
            maximum_retry_attempts = 3
            maximum_event_age_in_seconds = 3600
          }
        }
      ]
    }


    tags = {
      Name = "${var.fluxter_name}-eventbridge-hourly-trigger"
    }
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = module.lambda_hourly_trigger.eventbridge_rule_arns["hourly_lambda"]
}

resource "aws_sqs_queue" "dlq" {
    name = "${var.fluxter_name}-eventbridge-hourly-trigger-dlq"

    message_retention_seconds = 1209600
  }
