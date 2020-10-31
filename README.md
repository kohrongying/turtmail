# Turtmail Service

1. Takes an excel input and saves each (half) sheet as a pdf
2. Mails out pdf

Context: Sending out monthly payslips

## Setting up
- AWS Account and credentials for SES
- Python3 
- Windows environment
- Microsoft Excel

```bash
pip install -r requirements.txt
```

## Infra set up
- AWS Account
```bash
export AWS_PROFILE=personal
cd terraform
terraform plan
terraform apply
```

## Running program
```bash
set aws_access_key_id=access-key-id
set aws_secret_access_key=secret-access-key

python main.py sample.xlsx

python main.py sample.xlsx --send-email
```

## Important to note:
- use AWS SES configuration set to monitor email delivery