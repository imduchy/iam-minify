import pytest

from src.truncate import truncate, merge_overlaps


class TestTruncateMethod:
    def test_raises_error_when_all_actions_are_empty(self):
        with pytest.raises(ValueError):
            truncate(all_actions=[], provided_actions=["lambda:CreateFunction"])

    def test_raises_error_when_trie_doesnt_contain_char(self):
        with pytest.raises(ValueError):
            truncate(
                all_actions=["lambda:CreateFunction"], provided_actions=["lambda:DestroyFunction"]
            )

    def test_returns_empty_list_when_provided_actions_are_empty(self):
        res = truncate(all_actions=["lambda:CreateFunction"], provided_actions=[])

        assert res == []

    def test_returns_action_without_wildcard_if_action_prefix_equals_action(self):
        res = truncate(
            all_actions=["lambda:CreateFunction", "lambda:CreateFunctionVersion"],
            provided_actions=["lambda:CreateFunction"],
        )

        assert res == ["lambda:CreateFunction"]

    def test_returns_action_with_wildcard_if_node_ocurrence_is_one(self):
        res = truncate(
            all_actions=["lambda:CreateFunction", "lambda:CreateFunctionVersion"],
            provided_actions=["lambda:CreateFunctionVersion"],
        )

        assert res == ["lambda:CreateFunctionV*"]


class TestMergeOverlapsMethod:
    def test_merge_two_overlapping_actions_into_one(self):
        res = merge_overlaps(
            all_actions=[
                "lambda:CreateFunction",
                "lambda:CreateFunctionVersion",
                "lambda:CreateAlias",
            ],
            truncated_actions=[
                "lambda:CreateFunction",
                "lambda:CreateFunctionV*",
            ],
        )

        assert res == ["lambda:CreateF*"]

    def test_no_wildcard_is_added_for_non_truncated_actions(self):
        res = merge_overlaps(
            all_actions=[
                "lambda:CreateFunction",
                "lambda:CreateFunctions",
                "lambda:CreateFunctionVersion",
            ],
            truncated_actions=["lambda:CreateFunction"],
        )

        assert res == ["lambda:CreateFunction"]

    def test_merge_multiple_overlaping_actions(self):
        res = merge_overlaps(
            all_actions=[
                "lambda:CreateAlias",
                "lambda:CreateFunction",
                "lambda:CreateFunctionVersion",
                "lambda:GetAlias",
                "lambda:GetFunction",
                "lambda:GetFunctionVersion",
            ],
            truncated_actions=[
                "lambda:CreateFunction",
                "lambda:CreateFunctionV*",
                "lambda:GetFunction",
                "lambda:GetFunctionV*",
            ],
        )

        assert res == ["lambda:CreateF*", "lambda:GetF*"]

    def test_action_names_are_sorted(self):
        res = merge_overlaps(
            all_actions=[
                "lambda:DeleteAlias",
                "lambda:CreateAlias",
                "lambda:GetAlias",
                "lambda:DeleteFunction",
                "lambda:CreateFunction",
                "lambda:GetFunction",
            ],
            truncated_actions=[
                "lambda:DeleteF*",
                "lambda:CreateF*",
                "lambda:GetF*",
                "lambda:DeleteA*",
                "lambda:GetA*",
                "lambda:CreateA*",
            ],
        )

        assert res == ["lambda:C*", "lambda:D*", "lambda:G*"]

    def test_return_action_without_wildcard_if_cant_be_merged(self):
        res = merge_overlaps(
            truncated_actions=["s3:ListBucket", "s3:ListBucketV*"],
            all_actions=[
                "s3:ListAllMyBuckets",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
                "s3:ListBucketVersions",
                "s3:ListJobs",
            ],
        )

        assert res == ["s3:ListBucket", "s3:ListBucketV*"]

    def test_return_single_action_without_wildcard(self):
        res = merge_overlaps(
            truncated_actions=["s3:ListBucket"],
            all_actions=[
                "s3:ListAllMyBuckets",
                "s3:ListBucket",
                "s3:ListBucketVersions",
                "s3:ListJobs",
            ],
        )

        assert res == ["s3:ListBucket"]
