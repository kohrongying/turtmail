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
- AWS Account required
```bash
export AWS_PROFILE=personal
cd terraform
terraform plan
terraform apply
```
1. Creates a SES Config set
2. Creates a SNS Topic for failed delivery -> triggers email sent (email subscription done manually)
3. Creates a SNS Topic for successful delivery -> triggers lambda function that logs output to Cloudwatch

## Running program
1. Git clone this repo
2. Set up python virtualenv

| Running on Windows: Create a batch script "Payslip.bat" with contents as per below. Run the batch file.
```commandline
"C:\Users\xxx\venv\Scripts\python.exe" "path/to/payslips-mailer-runner.py"
```
*TIP*: Use `where python` to get the path of python executable

| Running from command line
```bash
(venv) python payslip-mailer-runner.py
```


## Important to note:
- use AWS SES configuration set to monitor email delivery
- SES pricing: $0.10 for every 1,000 emails sent/mth
- SNS pricing: 1,000 email notifications/mth (free tier), no charges to lambda (1GB/mth free data transfer out of SNS)
- Lambda pricing: $0.20 per 1M requests/mth, $0.17 per 10,000 GB-seconds of compute time/mth