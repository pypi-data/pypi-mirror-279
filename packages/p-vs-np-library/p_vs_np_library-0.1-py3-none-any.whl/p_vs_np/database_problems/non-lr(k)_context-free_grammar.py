#Non-LR(K) Context-Free Grammar

def is_non_lr_k_grammar(grammar, k):
    # Convert the grammar to augmented grammar
    augmented_grammar = convert_to_augmented_grammar(grammar)

    # Generate all possible items
    items = generate_items(augmented_grammar, k)

    # Check if there are any shift-reduce conflicts
    for item in items:
        lookahead_symbols = get_lookahead_symbols(item, k)
        shift_symbols = item['shift_symbols']
        reduce_symbols = item['reduce_symbols']

        # Check if there are any shift-reduce conflicts
        if set(shift_symbols).intersection(reduce_symbols):
            return True

        # Check if there are any reduce-reduce conflicts
        if len(reduce_symbols) > 1:
            return True

    return False


def convert_to_augmented_grammar(grammar):
    augmented_grammar = grammar.copy()

    # Add a new start symbol and production rule
    start_symbol = 'S\''
    augmented_grammar[start_symbol] = [grammar['start_symbol']]

    return augmented_grammar


def generate_items(grammar, k):
    items = []

    # Add the initial item
    start_production = grammar['S\''][0]
    initial_item = {'production': start_production, 'position': 0, 'lookahead': ['$']}
    items.append(initial_item)

    # Generate the closure of each item
    for item in items:
        closure_items = closure(grammar, item, k)
        items.extend(closure_items)

    return items


def closure(grammar, item, k):
    closure_items = []
    items_to_process = [item]

    while items_to_process:
        current_item = items_to_process.pop(0)
        production = current_item['production']
        position = current_item['position']
        lookahead = current_item['lookahead']

        if position < len(production):
            next_symbol = production[position]

            if next_symbol in grammar:
                # Non-terminal symbol, add new items
                for production in grammar[next_symbol]:
                    new_item = {'production': production, 'position': 0, 'lookahead': lookahead}
                    if new_item not in closure_items:
                        closure_items.append(new_item)
                        items_to_process.append(new_item)

                    if lookahead != ['$']:
                        # Add lookahead to new items
                        for i in range(1, k + 1):
                            new_lookahead = lookahead[:i] + ['$']
                            new_item = {'production': production, 'position': 0, 'lookahead': new_lookahead}
                            if new_item not in closure_items:
                                closure_items.append(new_item)
                                items_to_process.append(new_item)

            elif next_symbol == '':
                # End of production, add reduce symbol
                reduce_symbol = production[0]
                if reduce_symbol not in lookahead:
                    lookahead.append(reduce_symbol)

    return closure_items


def get_lookahead_symbols(item, k):
    lookahead = item['lookahead']

    # Get the distinct lookahead symbols up to k
    if lookahead == ['$']:
        return lookahead
    else:
        return lookahead[:k]


# Example usage
grammar = {
    'start_symbol': 'S',
    'S': ['aS', 'bA'],
    'A': ['bA', '']
}

k = 1

non_lr_k = is_non_lr_k_grammar(grammar, k)
print(f"Non-LR({k}) Grammar: {non_lr_k}")

