"""Custom selection with colored highlight"""

from pick import pick as pick_lib


def select_item(items, title="Select an item:", indicator="►"):
    """
    Selection with arrow keys
    
    Args:
        items: List of items to select from
        title: Selection prompt title
        indicator: Indicator character (default: ►)
    
    Returns:
        Selected item and its index
    """
    selected, index = pick_lib(items, title, indicator=indicator)
    return selected, index


def select_multiple(items, title="Select items:", indicator="►"):
    """
    Multi-selection with arrow keys
    
    Args:
        items: List of items to select from
        title: Selection prompt title
        indicator: Indicator character (default: ►)
    
    Returns:
        List of selected items
    """
    selected = pick_lib(items, title, multiselect=True, indicator=indicator)
    
    # Extract item names from tuples if multiselect
    if selected and isinstance(selected[0], tuple):
        selected = [item[0] for item in selected]
    
    return selected
