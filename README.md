# HYP Membership Portal

The HYP membership portal is a static web app built to manage membership data and new member applications. The project is built using Typescript and [Next.js](https://nextjs.org/), A [React](https://react.dev/) based framework for full stack web applications. This project makes up the frontend portion of the HYP Membership Platform. The backend portion which this app interfaces with is the [membership api](https://github.com/hyp-admin/membership-api). More information about the api can be found in that projects README.

The application is deployed as an AWS S3 static website. A guide on accessing AWS and managing our AWS resources can be found in the [Membership Platform Overview & User Guide](https://docs.google.com/document/d/13KspsvrRANksA_iWkb91knpWMdOuwDMPY5Ottvcl85o/edit?usp=sharing). Login credentials are injected into the application via environmnent variables at build time and up to date credentials should be stored in HYP password manager. More information on how to change credentials can be found in the Environment Variables section.

## Getting Started

It is recommended to install the following software in an isolated development environment such as a virutal machine to prevent conflicts with pre existing software on your machine. [Follow this guide](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview) to setup an Ubuntu (Linux) virtual machine with VirtualBox.

To build and deploy the application you will need to first install a few things.

- [Git](https://git-scm.com/downloads) - Version control software used to track changes to code. You will need to this to pull the project source code to your machine and push any changes to the remote repository. Git branches are also used to target deployment environments. Follow the installation instructions for your operating system.
- [Node and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm#using-a-node-version-manager-to-install-nodejs-and-npm) - Use these instruction to install Node and npm through a node version manager.
  - `node` - A Javascript/Typescript runtime. This is needed to generate the applications static assets.
  - `npm` - Javascript package management software. This is needed to download and install project depenedencies.
- [Docker](https://docs.docker.com/get-docker/) - Virtualisation software for containerised environments. This is used to ensure consistent builds and streamline the deployment process.
- [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) - Tool for interacting with AWS services via the command line. This is needed for running deployment scripts and ad hoc AWS operations.

## Development

Clone this repository to your machine. If you haven't already, you should create a directory to house this and other hyp repositories.

e.g.

```
mkdir hyp
cd hyp
git clone https://github.com/hyp-admin/membership-portal.git
```
Notes: 
* You may be prompted to authenticate to github. It is recommended to [generate a Github Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) for your personal use to track responsibility for code changes. You will need to login the hypadmin github account to generate a token or use the root (not recommended) token to authenticate. These credentials can be found in the HYP password manager.

Next, navigate to the project root and install dependencies.
```
cd membership-portal
npm install
```

Then, generate static assets to the `out` directory.

```
npm run build
```

Once the project has been built successfully, the application can be navigated to using a browser via the `File` URI scheme.

```
File:///<path>/<to>/<out>/<directory>/index.html
```
Notes: 
* Environment variables must be configured for the application to work properly. See the Environment Variables section below.
* You may need to enable use of the File URI scheme in your browser settings.
* Changes to code require static assets to be regenerated.


## Deployment

The Membership Portal is deployed as a [S3 Static Website](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html). A deployment can triggered by running the deployment script.

```
scripts/deploy.sh
````

There are currently two S3 buckets configured to host the app.

| Bucket                 | Environment | Description                                                                                                                              | URL                                                                     |
|------------------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| membership-portal-main | Production  | This is our production environment. This bucket should not be deleted under any circumstance other than to decommission the application. | `http://membership-portal-main.s3-website-ap-southeast-2.amazonaws.com` | 
| membership-portal-test | Test        | This is our testing environment. This bucket is intended to be used for testing new changes before they are rolled out to production.    | `http://membership-portal-test.s3-website-ap-southeast-2.amazonaws.com` |

The deployment script uses the current git branch to target which environment the generated static assets are deployed to. For example, if you have `main` checked out, running `./scripts/deploy.sh` via the command line will deploy to the production environment. Deployments adhere to the following pattern.

* Bucket - `membership-portal-<branch>`
* URL - `http://membership-portal-<branch>.s3-website-ap-southeast-2.amazonaws.com`

Notes:
* You will need to be authenticated to AWS to successfully deploy the project to S3. Use the aforementioned AWS guide to do this.
* You can create extra environments by configuring another S3 bucket and creating a new git branch.
* Testing environments should never be used to call prod membership-api endpoints.

## Environment Variables

Environment variables are used in this project to configure credentials and membership-api endpoints. Before running the deployment script or generating static assets, you will need to create a `.env` file in the project root directory containing these values. Default configuration values for this file (for both production and test environments) can be found in the password manager. The following is a description of each variable.

| Name     | Description                                                                                  |
|----------|----------------------------------------------------------------------------------------------|
| STAGE    | Used for environment specific configuration. Usually the same as your git branch.            |
| BASE_URL | The base URL for the membership-api. Determines which membership-api endpoints are targeted. |
| API_KEY  | Credential key for the target membership-api endpoints.                                      |
| APP_USER | Application username. Use this on the login screen.                                          |
| PASSWORD | Application password. Use this on the login screen.                                          |


