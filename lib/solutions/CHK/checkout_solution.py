

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    # Define prices dictionary (could be defined in a different module for modularity)
    prices_dict = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15,
        'E': 40
    }
    # Special offers are now ordered from best to worst
    # NOTE: The algorithm relies on each list of offers being ordered from highest
    # to lowest quantities
    special_offers_dict = {
        'A': [{'quantity': 5, 'total_price': 200},
              {'quantity': 3, 'total_price': 130}],
        'B': [{'quantity': 2, 'total_price': 45}],
    }
    cross_sale_offers_dict = {
        'E': {'quantity': 2, 
              'target_sku_sale': 'B', 
              'target_sku_reduction_quantity': 1}
    }


    # Count items in basket and error if there are new items not present in LUTs
    basket = {}
    for sku in skus:
        if not sku in prices_dict:
            print(-1) 
        basket[sku] = basket.get(sku, 0) + 1

    # The logic implies that getting one free in cross sales is always the best for the consumer
    # So you can do that first:
    for sku, values in cross_sale_offers_dict.items():
        # Calculate how many you need to remove from basket
        # (with a minimum of zero)
        if sku in basket:
            remove_from_basket = (basket[sku]  // values['quantity']) \
                * values['target_sku_reduction_quantity']
            basket[values['target_sku_sale']] = max(basket[values['target_sku_sale']] - remove_from_basket, 
                                                    0)

    # Check if any of the items in the basket has a special offer and compute
    # the offers first, sum the remainders. 
    # Otherwise just add the standard item * price
    final_checkout_basket = {}
    total_checkout = 0
    for sku, count in basket.items():
        payment = 0
        if sku in special_offers_dict:
            instrumental_count = count
            for offer_volume in special_offers_dict[sku]:
                if instrumental_count != 0:
                    total_packs = instrumental_count // offer_volume['quantity']    
                    payment += total_packs * offer_volume['total_price']
                    remainder = instrumental_count % offer_volume['quantity'] 
                    instrumental_count = remainder
            payment += remainder * prices_dict[sku]
            
        else: 
            payment = count * prices_dict[sku]
        
        final_checkout_basket[sku] = {'items': count, 'payment': payment}
        total_checkout += payment
            
    # Apply cross sales in case they exist: 

    return total_checkout

