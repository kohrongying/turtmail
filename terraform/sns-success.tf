resource "aws_sns_topic" "success" {
  name = "payslip-delivery-success"
}

resource "aws_ses_event_destination" "success_topic_dest" {
  name                   = "on-delivery-success"
  configuration_set_name = aws_ses_configuration_set.this.name
  enabled                = true
  matching_types         = ["delivery"]

  sns_destination {
    topic_arn = aws_sns_topic.success.arn
  }
}

resource "aws_sns_topic_policy" "success" {
  arn = aws_sns_topic.success.arn

  policy = data.aws_iam_policy_document.success_sns_topic_policy.json
}

resource "aws_sns_topic_subscription" "lambda" {
  topic_arn = aws_sns_topic.success.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.logger.arn
  endpoint_auto_confirms = true
}

data "aws_iam_policy_document" "success_sns_topic_policy" {
  policy_id = "__default_policy_ID"

  statement {
    actions = [
      "SNS:GetTopicAttributes",
      "SNS:SetTopicAttributes",
      "SNS:AddPermission",
      "SNS:RemovePermission",
      "SNS:DeleteTopic",
      "SNS:Subscribe",
      "SNS:ListSubscriptionsByTopic",
      "SNS:Receive",
      "SNS:Publish",
    ]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceOwner"

      values = [
        data.aws_caller_identity.current.id
      ]
    }

    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    resources = [
      aws_sns_topic.success.arn
    ]

    sid = "__default_statement_ID"
  }
}