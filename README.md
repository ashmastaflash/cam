# Raspberry Pi camera w/motion detection.

## Motion-detecting camera GPG-encrypts images and video, uploads all to S3.

This tool is designed to work with a USB webcam, and would probably work just
fine with the Pi camera module.  It expects the camera to be at `/dev/video0`.

## Requirements

* Hardware:
  * Linux-supported USB webcam
  * Raspberry Pi (tested on Pi 2, should work on any model, though)
    * 32GB storage
* Accounts:
  * Amazon AWS
  * Resin.io
* Assets:
  * S3 Bucket (for storing images and video)
  * API key with write access to the S3 bucket.
  * GPG key pair

## Setup and Usage

1. Clone this repository to your local machine.
1. Create an application in Resin.io for this project.
1. Add the Resin.io project as a git remote for the cloned repository.
1. Push the code to Resin.io (try `git push resin master`)
1. Configure environment variables for the project according to the table below.
1. Download and install the applcication image from Resin.io and install on your device(s).

### Environment Variables

| Variable                      | Purpose                                      |
|-------------------------------|----------------------------------------------|
| AWS_ACCESS_KEY_ID             | ID of API key with write access to S3 bucket |
| AWS_SECRET_ACCESS_KEY         | Secret corresponding to AWS_ACCESS_KEY_ID    |
| AWS_DEFAULT_REGION            | Region for AWS S3 bucket                     |
| GPG_PUBKEYS                   | Base-64 encoded pubkey from gpg export       |
| RECIPIENTS                    | Recipients (semicolon-separated) for pubkeys |
| S3_BUCKET                     | Name of S3 bucket to drop captures in        |
| USE_PI_CAMERA                 | If set, attempt to init onboard pi camera.   |

### Getting a Public Key from GPG/Keybase

https://github.com/pstadler/keybase-gpg-github

### Listing Installed GPG Keys
```
gpg --list-keys

```

### Base64 Encoding your GPG pubkey

```
gpg --export MY_KEY_ID | base64

```

### Downloading your images from S3

The easiest method is using the AWS CLI to download and the `gpg` command to
decrypt.

[AWS S3 CLI reference](http://docs.aws.amazon.com/cli/latest/reference/s3/)

[GPG Cheat Sheet](http://irtfweb.ifa.hawaii.edu/~lockhart/gpg/)
