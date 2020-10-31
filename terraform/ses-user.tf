# Use access keys of this user for ses service using boto3
resource "aws_iam_user" "ses_user" {
  name = "ses-user"
}
