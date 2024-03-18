from src.actions import IAMActions

from src.truncate import merge_overlaps, truncate

if __name__ == "__main__":
    all_actions = IAMActions()

    original_permissions = [
        "s3:DescribeJob",
        "s3:ListBucket",
        "s3:ListStorageLensConfigurations",
        "s3:ListAllMyBuckets",
        "s3:ListBucketMultipartUploads",
        "s3:ListJobs",
        "s3:ListMultipartUploadParts",
        "s3:ListBucketVersions",
        "s3:ListAccessPointsForObjectLambda",
        "s3:ListAccessPoints",
        "s3:ListMultiRegionAccessPoints",
        "s3:GetObject",
        "s3:GetObjectTorrent",
        "s3:GetObjectVersionForReplication",
        "s3:GetObjectVersionTorrent",
        "s3:GetEncryptionConfiguration",
        "s3:GetObjectTagging",
        "s3:GetObjectVersionTagging",
        "s3:GetObjectVersionAcl",
        "s3:GetObjectAcl",
        "s3:GetObjectVersion",
        "s3:CreateJob",
        "s3:ReplicateObject",
        "s3:DeleteJobTagging",
        "s3:DeleteObject",
        "s3:DeleteObjectTagging",
        "s3:DeleteStorageLensConfigurationTagging",
        "s3:DeleteObjectVersionTagging",
        "s3:DeleteObjectVersion",
        "s3:PutObject",
        "s3:PutBucketTagging",
        "s3:PutObjectTagging",
        "s3:PutStorageLensConfigurationTagging",
        "s3:PutObjectVersionTagging",
        "s3:PutJobTagging",
        "s3:AbortMultipartUpload",
        "s3:ReplicateTags",
        "s3:RestoreObject",
        "s3:UpdateJobPriority",
        "s3:UpdateJobStatus",
        "s3:GetBucketLocation",
        "s3:GetLifecycleConfiguration",
        "s3:PutLifecycleConfiguration",
        "s3:PutObjectAcl",
        "dynamodb:DescribeTable",
        "dynamodb:PartiQLInsert",
        "dynamodb:GetItem",
        "dynamodb:BatchGetItem",
        "dynamodb:BatchWriteItem",
        "dynamodb:PutItem",
        "dynamodb:PartiQLUpdate",
        "dynamodb:Scan",
        "dynamodb:UpdateItem",
        "dynamodb:GetShardIterator",
        "dynamodb:GetRecords",
        "dynamodb:ListTables",
        "dynamodb:ConditionCheckItem",
        "dynamodb:DeleteItem",
        "dynamodb:PartiQLSelect",
        "dynamodb:ListTagsOfResource",
        "dynamodb:Query",
        "dynamodb:DescribeStream",
        "dynamodb:ListStreams",
        "dynamodb:ListGlobalTables",
        "dynamodb:PartiQLDelete",
        "athena:BatchGetNamedQuery",
        "athena:BatchGetQueryExecution",
        "athena:CreateNamedQuery",
        "athena:DeleteNamedQuery",
        "athena:StartQueryExecution",
        "athena:StopQueryExecution",
        "timestream:SelectValues",
        "timestream:ListDatabases",
        "timestream:ListTables",
        "timestream:CancelQuery",
        "timestream:Select",
        "timestream:WriteRecords",
        "neptune-db:connect",
    ]

    truncated_permissions = truncate(
        provided_actions=original_permissions,
        all_actions=all_actions.as_list,
    )

    optimized_list = merge_overlaps(
        truncated_actions=truncated_permissions,
        all_actions=all_actions.as_list,
    )

    # assert truncated_permissions == ["lambda:DeleteA*", "lambda:CreateFunction", "lambda:DeleteFunctionCod*"]

    print("")
    print(f"Original permissions: {original_permissions}")
    print(f"Truncated permissions: {optimized_list}")
