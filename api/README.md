# Membership API

The membership API project is a monorepo containing a set of RESTful endpoints configured to perform CRUD operations on a PostgreSQL AWS RDS instance and an AWS DynamoDB table. The project consists of the membership and applications lambda functions that read and write to their respective database tables. The Lambda function are invoked by calls to an AWS API Gateway instance and secured by an API Key.

## Endpoints.

| URL Suffix                | HTTP Method | Description                                                                     |
|---------------------------|-------------|---------------------------------------------------------------------------------|
| {stage}/applications      | POST        | Adds submitted ‘become a member’ form data to the applications DynamoDB table.  |
| {stage}/applications/{id} | GET         | Retrieves all pending applications from the applications DynamoDB table.        |
| {stage}/applications/{id} | DELETE      | Deletes a single record from the applications DynamoDB table for the given ‘id’.|
| {stage}/membership        | GET         | Retrieves all records from the membership Postgres table.                       |
| {stage}/membership        | POST        | Adds a record to the membership Postgres table.                                 |
| {stage}/membership/{id}   | GET         | Retrieves a single record from the membership Postgres table for the given ‘id’.|
| {stage}/membership/{id}   | PUT         | Updates a single record from the membership Postgres table for the given ‘id’.  |
| {stage}/membership/{id}   | DELETE      | Deletes a single record from the membership Postgres table for the given ‘id’.  |

Notes
* The 'stage' part of the URL is the API Gateway stage which is derived from the current git branch when running the deployment script.

## Getting Started

It is recommended to install the following software in an isolated development environment such as a virutal machine to prevent conflicts with pre existing software on your machine. [Follow this guide](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview) to setup an Ubuntu (Linux) virtual machine with VirtualBox.

To build and deploy the application you will need to first install a few things.

- [Git](https://git-scm.com/downloads) - Version control software used to track changes to code. You will need to this to pull the project source code to your machine and push any changes to the remote repository. Git branches are also used to target deployment environments. Follow the installation instructions for your operating system.
- [Python](https://www.python.org/downloads/) - Programming language the membership api is coded in.
- [Docker](https://docs.docker.com/get-docker/) - Virtualisation software for containerised environments. This is used to ensure consistent builds and streamline the deployment process.
- [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) - Tool for interacting with AWS services via the command line. This is needed for running deployment scripts and ad hoc AWS operations.

## Development

Clone this repository to your machine. If you haven't already, you should create a directory to house this and other repositories.

e.g.

```
mkdir Code
cd Code
git clone https://github.com/JakeHerington/membership-api.git
```

## Deployment

Before deploying the membership api stack, you will need to build each projects .zip artifact. This can be done by executing the build script in each projects `/scripts` directory. E.g.

```
cd membership
./scripts/build.sh
```

This will create a .zip file containing the lambda function source code in the root directory of the membership-api project. Once the source code artifacts have been generated, execute the deployment script from the root directory. E.g.

```
./deploy.sh
```

The deployment script will assume the IAM deployer role and create/update a Cloudformation stack with the following resources.

* Application Lambda
* Application DynamoDB table
* Membership Lambda
* API Gateway
* API Gateway Usage Plan and API Key
* Membership API Lambda Execution IAM Role
* IAM Policies allowing for stack resources to interact

The Cloudformation stack is generated from the `sam_template.yml` file in the root directory and the API Gateway resource in the template file uses the `swagger.yml` file (also in the root directory) as the definition for the API endpoints.
The deployment script will also upload the .zip artifacts to an S3 bucket which will be used as the respective Lambda functions source code.

Notes:
* You will need to be authenticated to AWS to successfully deploy the project. Use the aforementioned AWS guide to do this.

### Testing

A suite of unit tests have been created with the unittest framework that ships with Python. The tests can be run by executing the following script in each sub repository. E.g.

```
cd membership
./scripts/run-tests.sh
```
