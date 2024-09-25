terraform {
  backend "s3" {
    bucket         = "meli-challenge-tl2" # Use the exact bucket name created
    key            = "meli-challenge/state/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock-table" # Use the exact DynamoDB table name created
  }
}

provider "aws" {
  region = "us-east-1"
}

module "kube_infrastructure" {
  source = "./modules/kube-infra"
}
