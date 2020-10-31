provider "aws" {
  version = "~> 3.0"
  region  = "ap-southeast-1"
}

terraform {
  backend "s3" {
    bucket = "ry-terraform-state"
    key    = "payslip-email-service/terraform.tfstate"
    region = "ap-southeast-1"
  }
}