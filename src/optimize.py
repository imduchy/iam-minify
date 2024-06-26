import logging
from src.trie import Trie, TrieNode

LOGGER = logging.getLogger("iam-minify")


class UnsupportedWildcardError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NonExistentActionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def truncate(provided_actions: list[str], all_actions: list[str]):
    base_trie = Trie.from_list(all_actions)

    truncated_list = []

    # Loop through the provided IAM actions and find the longest prefix that exists in the trie.
    for action in provided_actions:
        service_prefix = action.split(":")[0]

        action_prefix = ""
        node: TrieNode = base_trie.root

        for pos, char in enumerate(action):
            # If the provided action contains a star (wildcard) at the end of the string, we can
            # break from the loop and return the value as is.
            if char == "*":

                # TODO: Support wildcards in the middle of a string
                if pos != len(action) - 1:
                    raise UnsupportedWildcardError(
                        f"IAM action {action} couldn't be truncated. Wildcard characters in the "
                        f"middle of the string are not supported."
                    )

                truncated_list.append(action)
                break

            if not char in node.children:
                raise NonExistentActionError(
                    f"IAM action {action} couldn't be truncated. Character {char} at position "
                    f"{pos} doesn't exist in the trie."
                )

            node: TrieNode = node.children[char]
            action_prefix += char

            # If the truncated string equals to the actual IAM action name, we can break from the
            # loop and return the value without the wildcard at the end.
            if action_prefix == action:
                truncated_list.append(action_prefix)
                break

            # If the occurences of the character in the trie is 1, it means that there are no other
            # IAM actions with the same prefix, so we can break from the loop and return the value
            # with the wildcard at the end.
            if pos > len(service_prefix) and node.occurences == 1:
                truncated_list.append(action_prefix + "*")
                break

    return truncated_list


def merge_overlaps(truncated_actions: list[str], all_actions: list[str]) -> list[str]:
    truncated_trie = Trie.from_list(truncated_actions)
    base_trie = Trie.from_list(all_actions)

    optimized_actions = []

    for action in truncated_actions:
        truncated_node: TrieNode = truncated_trie.root
        base_node: TrieNode = base_trie.root

        service_prefix = action.split(":")[0]
        action_prefix = ""

        for index, char in enumerate(action):
            # If the character is a star (wildcard), it means we're at the end of the string and
            # there's nothing to optimize
            if char == "*":
                break

            truncated_node: TrieNode = truncated_node.children[char]
            base_node: TrieNode = base_node.children[char]

            action_prefix = action_prefix + char

            # There's nothing to optimze at the service prefix, so continue until we get past that
            if index <= len(service_prefix) - 1:
                continue

            # If the current prefix equals to the truncated action, we can break from the
            # loop and return the value without the wildcard at the end.
            if action_prefix == action and truncated_node.occurences < base_node.occurences:
                optimized_actions.append(action)
                break

            # If the occurences of a character in both tries are equal, it means there are no
            # other unintended IAM actions in the list of `all_actions` with the same prefix. In
            # such case, we can further truncate the prefix at the current position.
            if truncated_node.occurences == base_node.occurences:
                optimized_actions.append(action_prefix + "*")
                break

    # Remove duplicates from the list
    optimized_actions = list(set(optimized_actions))

    # Sort the list for predictable results
    optimized_actions.sort()

    return optimized_actions
