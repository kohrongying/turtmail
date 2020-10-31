resource "aws_sns_topic" "fail" {
  name = "payslip-delivery-failure"
}

resource "aws_ses_event_destination" "fail_topic_dest" {
  name                   = "on-delivery-failure"
  configuration_set_name = aws_ses_configuration_set.this.name
  enabled                = true
  matching_types         = ["reject", "bounce", "complaint", "renderingFailure"]

  sns_destination {
    topic_arn = aws_sns_topic.fail.arn
  }
}

resource "aws_sns_topic_policy" "fail" {
  arn = aws_sns_topic.fail.arn

  policy = data.aws_iam_policy_document.fail_sns_topic_policy.json
}

data "aws_iam_policy_document" "fail_sns_topic_policy" {
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
      aws_sns_topic.fail.arn
    ]

    sid = "__default_statement_ID"
  }
}

data "aws_caller_identity" "current" {}

// To Email (not supported - add yourself)
//resource "aws_sns_topic_subscription" "email_subscription" {
//  topic_arn = aws_sns_topic.fail.arn
//  protocol  = "email"
//}