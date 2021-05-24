# TODO: change region in provider, availability_zone in subnet, accesskey and secretkey, add token

terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 3.0"
        }
    }
}

variable "aws_access_key" {
    description = "Access Key to your AWS account"
    type        = string
}

variable "aws_secret_key" {
    description = "Secret Key to your AWS account"
    type        = string
}

variable "aws_region" {
    description = "Region to your AWS account"
    type        = string
    default     = "us-east-2"
}

variable "aws_s3_bucket_name" {
    description = "S3 Bucket name"
    type        = string
}

# AWS Provider
provider "aws" {
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
    region = var.aws_region
}

# IAM Policy for Redshift
data "aws_iam_policy_document" "redshift_policy" {
    statement {
        actions = ["sts:AssumeRole"]
        principals {
          type = "Service"
          identifiers = [ "redshift.amazonaws.com" ]
        }
    }
}

# IAM Role
resource "aws_iam_role" "redshift_role" {
    name = "myRedshiftRole"
    description = "Allows Redshift clusters to call AWS services on your behalf"
    assume_role_policy = data.aws_iam_policy_document.redshift_policy.json
}

# Attaching Policy to IAM Role
resource "aws_iam_role_policy_attachment" "s3-read-only-policy-att" {
    role =  aws_iam_role.redshift_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
    depends_on = [
        aws_iam_role.redshift_role
    ]
}

# Default VPC
resource "aws_default_vpc" "default_vpc" {
    tags = {
      "Name" = "Default VPC"
    }
}

# Security Group
resource "aws_security_group" "redshift_security_group" {
    name = "redshift_security_group"
    description = "Authorise redshift cluster access"
    vpc_id = aws_default_vpc.default_vpc.id

    ingress {
        from_port        = 5439
        to_port          = 5439
        protocol         = "tcp"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    egress {
        from_port        = 0
        to_port          = 0
        protocol         = "-1"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    depends_on = [
        aws_default_vpc.default_vpc
    ]
}

# Subnets
resource "aws_subnet" "subnet_one" {
    cidr_block        = "172.31.48.0/20"
    availability_zone = "us-east-2a"
    vpc_id            = aws_default_vpc.default_vpc.id
    map_public_ip_on_launch = true

    depends_on = [
        aws_default_vpc.default_vpc
    ]
}

resource "aws_subnet" "subnet_two" {
    cidr_block        = "172.31.64.0/20"
    availability_zone = "us-east-2b"
    vpc_id            = aws_default_vpc.default_vpc.id
    map_public_ip_on_launch = true

    depends_on = [
        aws_default_vpc.default_vpc
    ]
}

# Redshift subnet group
resource "aws_redshift_subnet_group" "redshift_subnet" {
    name = "redshift-subnet"
    subnet_ids = [ aws_subnet.subnet_one.id, aws_subnet.subnet_two.id ]

    depends_on = [
        aws_subnet.subnet_one, aws_subnet.subnet_two
    ]
}

# Redshift cluster
resource "aws_redshift_cluster" "redshift_cluster" {
    cluster_identifier = "redshift-cluster-1"
    database_name      = "dev"
    port = 5439
    master_username    = "awsuser"
    master_password    = "RedshiftPass123"
    node_type          = "dc1.large"
    cluster_type       = "single-node"
    cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet.id
    iam_roles = [ aws_iam_role.redshift_role.arn ]
    vpc_security_group_ids = [ aws_security_group.redshift_security_group.id ]
    enhanced_vpc_routing = false
    publicly_accessible = true
    skip_final_snapshot = true

    depends_on = [
        aws_redshift_subnet_group.redshift_subnet,
        aws_iam_role.redshift_role,
        aws_security_group.redshift_security_group
    ]
}

# S3 Bucket
resource "aws_s3_bucket" "s3_bucket" {
    bucket = var.aws_s3_bucket_name
}
