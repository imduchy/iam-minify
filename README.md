# IAM Policies minifier

Optimize long AWS IAM policies by strategically using wildcards, reducing the number of characters, and maintaining the intended scope of permissions.

## Background & Rationale

When crafting long and complex AWS IAM customer-managed policies, the 6,144 character limit imposed by AWS can become a problem. While one approach to address this limitation is to split a long policy into multiple customer-managed policies, this may not always be the ideal solution. In such scenarios, it's possible to reduce the length of a policy by strategically using wildcards where possible.

The `iam-minify`-er traverses through a list of IAM actions defined in a policy, identifies optimal locations for wildcards, and effectively reduces the character count while maintaining the intended permission scope.

## Instalation

```
python -m pip install iam-minify
```

## Usage & features

- `iam-minify -f path/to/policy.json` 

The script will traverse though all policy statemends defined in the policy document, and optimise IAM actions within the same statement. It processes different policy statements in isolation in order to not grant unintended access to resources.

Consider the following IAM policy:

```json
// ./myPolicy.json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:ListStorageLensConfigurations",
        "s3:ListAllMyBuckets",
        "s3:ListBucketMultipartUploads",
        "s3:ListJobs",
        "s3:ListMultipartUploadParts",
        "s3:ListBucketVersions",
        "s3:ListAccessPointsForObjectLambda",
        "s3:ListAccessPoints",
        "s3:ListMultiRegionAccessPoints"
      ],
      "Resource": "*"
    }
  ]
}
```

```bash
iam-minify -f myPolicy.json
```

Will output the following result:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListAccessP*",
        "s3:ListAl*",
        "s3:ListB*",
        "s3:ListJ*",
        "s3:ListM*",
        "s3:ListStorageLensC*"
      ],
      "Resource": "*"
    }
  ]
}
```