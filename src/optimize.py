from src.trie import Trie, TrieNode


def truncate(provided_actions: list[str], all_actions: list[str]):
    base_trie = Trie.from_list(all_actions)

    truncated_list = []

    # Loop through the provided IAM actions and find the longest prefix that exists in the trie.
    for action in provided_actions:
        service_prefix = action.split(":")[0]

        action_prefix = ""
        node: TrieNode = base_trie.root

        for pos, char in enumerate(action):
            if char not in node.children:
                raise ValueError(
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
            if pos > len(service_prefix) + 1 and node.occurences == 1:
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
        # Length of the service prefix (e.g., 'lambda:'), including the colon
        service_prefix_len = len(service_prefix) + 1
        action_prefix = ""

        for index, char in enumerate(action):
            # If the character is a star (wildcard), it means we're at the end of the string and
            # there's nothing to optimize
            if char == "*":
                break

            truncated_node: TrieNode = truncated_node.children[char]
            base_node: TrieNode = base_node.children[char]

            action_prefix += char

            # If the current prefix equals to the truncated action, we can break from the
            # loop and return the value without the wildcard at the end.
            if action_prefix == action and truncated_node.occurences < base_node.occurences:
                optimized_actions.append(action)
                break

            # If the occurences of a character in the truncated trie is 1, it means that there are
            # no other truncated actions with the same prefix, therefore, there's nothing to merge.
            if truncated_node.occurences == 1:
                optimized_actions.append(action)
                break

            # If the occurences of a character in both tries are equal, it means there are no
            # other unintended IAM actions in the list of `all_actions` with the same prefix. In
            # such case, we can further truncate the prefix at the current position.
            if index >= service_prefix_len and truncated_node.occurences == base_node.occurences:
                optimized_actions.append(action_prefix + "*")
                break

    # Remove duplicates from the list
    optimized_actions = list(set(optimized_actions))

    # Sort the list for predictable results
    optimized_actions.sort()

    return optimized_actions
