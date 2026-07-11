def print_trie(trie):
    print("*")
    items = sorted(trie.root.children.items())
    for i, (ch, child) in enumerate(items):
        is_last = (i == len(items) - 1)
        _print_node(child, prefix="", is_last=is_last, label=ch)


def _compress_chain(node, first_label):
    """
    Compress a single-child chain into:
      [ 'f', 'l', 'i', ... ]  ->  ['f', 'l', 'i', ...]
    but each element has '*' suffix if it's an end node (except root).
    Returns:
      parts (list of 'label' or 'label*'),
      last_node (TrieNode at end of chain)
    """
    parts = [first_label + ("*" if node.isEnd else "")]
    cur = node

    # Keep going as long as there's exactly one child.
    # We DO allow passing through isEnd nodes so that:
    #   o ── w* ── e ── r*
    # stays on one line.
    while len(cur.children) == 1:
        (ch, nxt), = cur.children.items()
        cur = nxt
        parts.append(ch + ("*" if cur.isEnd else ""))

    return parts, cur


def _print_node(node, prefix, is_last, label):
    parts, last_node = _compress_chain(node, label)
    chain_str = " ── ".join(parts)

    connector = "└── " if is_last else "├── "
    line = prefix + connector + chain_str
    print(line)

    # Children of the last node in the chain
    items = sorted(last_node.children.items())
    if not items:
        return

    # Align children under the START of the last segment.
    # Example:
    # "└── f ── l"
    #  total length = len(prefix) + len(connector) + len(chain_str)
    #  last_part = "l"
    #  we want '├' directly under 'l'
    last_part = parts[-1]
    spaces = len(prefix) + len(connector) + len(chain_str) - len(last_part)
    child_prefix = " " * spaces

    for i, (ch, child) in enumerate(items):
        child_last = (i == len(items) - 1)
        _print_node(child, child_prefix, child_last, ch)
