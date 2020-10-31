resource "aws_lambda_function" "logger" {
  function_name = "payslip-delivery-success-logger-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.handler"
  runtime = "nodejs12.x"
  filename = "lambda_function.zip"
}

resource "aws_lambda_permission" "with_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.logger.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.success.arn
}


resource "aws_iam_role" "iam_for_lambda" {
  name = "payslip-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_iam_policy" "lambda_basic_exec_role" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_exec_role_attachment" {
  policy_arn = data.aws_iam_policy.lambda_basic_exec_role.arn
  role = aws_iam_role.iam_for_lambda.name
}

resource "aws_cloudwatch_log_group" "lambda_log" {
  name = "/aws/lambda/${aws_lambda_function.logger.function_name}"
  retention_in_days = 60
}