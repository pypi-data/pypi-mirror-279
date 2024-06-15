def contain_all_items(my_list, items_to_check) -> bool:
    """
    Check if a list contains all items from another list.

    Args:
        my_list (list): The list to check.
        items_to_check (list): The list of items to check for.

    Returns:
        bool: True if my_list contains all items from items_to_check, False otherwise.
    """
    return all(item in my_list for item in items_to_check)

def contain_any_items(my_list, items_to_check) -> bool:
    """
    Check if a list contains all items from another list.

    Args:
        my_list (list): The list to check.
        items_to_check (list): The list of items to check for.

    Returns:
        bool: True if my_list contains all items from items_to_check, False otherwise.
    """
    return any(item in my_list for item in items_to_check)