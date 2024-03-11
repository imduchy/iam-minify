import json
from src.trie import Trie, TrieNode


def build_trie(actions: list[str]) -> Trie:
    trie = Trie()

    for action in actions:
        trie.insert(action)

    return trie


def truncate(provided_actions: list[str], trie_root: TrieNode):
    truncated_list = []

    # Loop through the provided IAM actions and find the longest prefix that exists in the trie.
    for action in provided_actions:
        prefix = ""
        node = trie_root

        for pos, char in enumerate(action):
            if char not in node.children:
                raise ValueError(
                    f"IAM action {action} couldn't be truncated. Character {char} at position "
                    f"{pos} doesn't exist in the trie."
                )

            node: TrieNode = node.children[char]
            prefix += char

            # If the truncated string equals to the actual IAM action name, we can break from the
            # loop and return the value without the wildcard at the end.
            if prefix == action:
                print(
                    f"(Breaking from the loop) IAM action {action} can't be truncated. The "
                    "wildcard won't be used."
                )
                truncated_list.append(prefix)
                break

            # If the occurences of the character in the trie is 1, it means that there are no other
            # IAM actions with the same prefix, so we can break from the loop and return the value
            # with the wildcard at the end.
            if node.occurences == 1:
                print(
                    f"(Breaking from the loop) Character {char} for prefix {prefix} at position "
                    f"{pos} has exactly one occurence in the trie."
                )

                prefix = prefix + "*"
                truncated_list.append(prefix)
                break

    return truncated_list


if __name__ == "__main__":
    # https://awspolicygen.s3.amazonaws.com/js/policies.js
    with open("./actions/lambda.json", mode="r", encoding="utf-8") as file:
        lambda_actions = json.loads(file.read())

    original_permissions = [
        "DeleteAlias",
        "CreateFunction",
        "DeleteFunctionCodeSigningConfig",
    ]

    trie = build_trie(lambda_actions["data"])

    truncated_permissions = truncate(
        provided_actions=original_permissions,
        trie_root=trie.root,
    )

    assert truncated_permissions == ["DeleteA*", "CreateFunction", "DeleteFunctionCod*"]

    print("")
    print(f"Original permissions: {original_permissions}")
    print(f"Truncated permissions: {truncated_permissions}")
