

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    # Define prices dictionary (could be defined in a different module for modularity)
    prices_dict = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15
    }
    special_offers_dict = {
        'A': {'quantity': 3, 'total_price': 130},
        'B': {'quantity': 2, 'total_price': 45},
    }

    # Count items in basket and error if there are new items not present in LUTs
    basket = {}
    for sku in skus:
        if not sku in prices_dict:
            return -1
        basket[sku] = basket.get(sku, 0) + 1

    # Check if any of the items in the basket has a special offer and compute
    # the offers first, sum the remainders. 
    # Otherwise just add the standard item * price
    final_checkout = 0
    for sku, count in basket.items():
        if sku in special_offers_dict:
            total_packs = count // special_offers_dict[sku]['quantity']
            remainder = count % special_offers_dict[sku]['quantity']
            payment = total_packs * special_offers_dict[sku]['total_price'] + \
                remainder * prices_dict[sku]
        else: 
            payment = count * prices_dict[sku]
        final_checkout += payment
            
    return final_checkout


