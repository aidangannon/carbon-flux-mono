resource "aws_s3_bucket" "blob" {
  bucket_prefix = "${var.name}-blob"
}

resource "aws_dynamodb_table" "db" {
  name           = "${var.name}-db"
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
    Name = "${var.name}-db"
  }
}
