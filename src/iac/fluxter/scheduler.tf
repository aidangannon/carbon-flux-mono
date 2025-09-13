module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = var.name
  description   = "Manages tracking site's for raw etc data"
  handler       = "src.fluxter_scrape.handler.handle"
  runtime       = var.python_runtime

  timeout = 30

  layers = [
    var.core_layer_arn
  ]

  create_package         = false
  local_existing_package = "../../dist/src.fluxter_scrape/lambda.zip"

  attach_policy_statements = true
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
    ICOS_USERNAME = var.icos_username
    ICOS_PASSWORD = var.icos_password
    HOME          = "/tmp"
  }

  tags = {
    Name = var.name
  }
}

module "lambda_hourly_trigger" {
  source = "terraform-aws-modules/eventbridge/aws"
  create_bus = false
  rules = {
    hourly_lambda = {
      name                = "${var.name}-hourly-trigger"
      description         = "Trigger ${var.name} every hour"
      schedule_expression = "cron(0 */1 * * ? *)"
    }
  }
  targets = {
    hourly_lambda = [
      {
        name = "lambda-target"
        arn  = module.lambda_function.lambda_function_arn
        dead_letter_arn = aws_sqs_queue.eventbridge-dlq.arn
        retry_policy = {
          maximum_retry_attempts = 3
          maximum_event_age_in_seconds = 3600
        }
      }
    ]
  }
  tags = {
    Name = "${var.name}-hourly-trigger"
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
  name = "${var.name}-eventbridge-hourly-trigger-dlq"
  message_retention_seconds = 1209600
}