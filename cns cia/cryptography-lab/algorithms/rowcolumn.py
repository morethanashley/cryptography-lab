# Row and Column Transposition Cipher
# Writes plaintext into a grid row by row, then reads columns in key order.
# The key determines the order in which columns are read.

def get_column_order(key):
    """
    Determine column reading order based on alphabetical order of key characters.
    e.g., key='DCBA' -> order=[3,2,1,0]
    """
    key = key.upper()
    indexed = sorted(enumerate(key), key=lambda x: x[1])
    order = [i for i, _ in indexed]
    return order


def encrypt(text, key):
    """
    Encrypt using Row-Column Transposition.
    Fill grid row by row, read columns in key-sorted order.
    """
    key = key.upper()
    cols = len(key)
    text = text.replace(' ', '').upper()
    # Pad with X if needed
    while len(text) % cols != 0:
        text += 'X'

    rows = len(text) // cols
    grid = [list(text[i*cols:(i+1)*cols]) for i in range(rows)]
    order = get_column_order(key)

    result = ''
    for col in order:
        for row in grid:
            result += row[col]

    return {
        "result": result,
        "grid": grid,
        "key": key,
        "column_order": order,
        "rows": rows,
        "cols": cols
    }


def decrypt(text, key):
    """
    Decrypt Row-Column Transposition.
    Reverse the column reading process to reconstruct the grid.
    """
    key = key.upper()
    cols = len(key)
    n = len(text)
    rows = n // cols
    order = get_column_order(key)

    # Determine how many chars go in each column
    grid = [[''] * cols for _ in range(rows)]
    idx = 0
    for col in order:
        for row in range(rows):
            grid[row][col] = text[idx]
            idx += 1

    result = ''.join(''.join(row) for row in grid)

    return {
        "result": result,
        "grid": grid,
        "key": key,
        "column_order": order
    }
