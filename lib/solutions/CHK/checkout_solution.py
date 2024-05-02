

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    
    # Define prices dictionary (could be defined in a different module for modularity)
    prices_dict = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15,
        'E': 40,
        'F': 10,
        'G': 20,
        'H': 10,
        'I': 35,
        'J': 60,
        'K': 70,
        'L': 90,
        'M': 15,
        'N': 40,
        'O': 10,
        'P': 50,
        'Q': 30,
        'R': 50,
        'S': 20,
        'T': 20,
        'U': 40,
        'V': 50, 
        'W': 20,
        'X': 17, 
        'Y': 20,
        'Z': 21
    }
    # Special offers are now ordered from best to worst
    # NOTE: The algorithm relies on each list of offers being ordered from highest
    # to lowest quantities
    special_offers_dict = {
        'A': [{'quantity': 5, 'total_price': 200}, 
              {'quantity': 3, 'total_price': 130}],
        'B': [{'quantity': 2, 'total_price': 45}],
        'H': [{'quantity': 10, 'total_price': 80},
              {'quantity': 5, 'total_price': 45}],
        'K': [{'quantity': 2, 'total_price': 120}],
        'P': [{'quantity': 5, 'total_price': 200}],
        'Q': [{'quantity': 3, 'total_price': 80}],
        'V': [{'quantity': 3, 'total_price': 130}, 
              {'quantity': 2, 'total_price': 90}]
    }
    # Dictionary of get n free after purchasing m products, can reference other
    # products
    get_free_products_offers_dict = {
        'E': {'quantity': 2, 
              'target_sku_sale': 'B', 
              'target_sku_reduction_quantity': 1},
        'F': {'quantity': 3, 
              'target_sku_sale': 'F', 
              'target_sku_reduction_quantity': 1},
        'N': {'quantity': 3, 
              'target_sku_sale': 'M', 
              'target_sku_reduction_quantity': 1},
        'R': {'quantity': 3, 
              'target_sku_sale': 'Q', 
              'target_sku_reduction_quantity': 1},
        'U': {'quantity': 4, 
              'target_sku_sale': 'U', 
              'target_sku_reduction_quantity': 1}
    }
    # Create a separate dictionary for bundle offers
    bundle_offers_dict = [{
            'items': ['S', 'T', 'X', 'Y', 'Z'],
            'quantity': 3, 
            'total_price': 45
        }]
    
    # Automatically reorder special_offers so that the biggest come first:
    # The algorithm below relies on this being ordered
    for sku in special_offers_dict.keys():
        special_offers_dict[sku] = sorted(special_offers_dict[sku], 
                                key = lambda x: x['total_price'], 
                                reverse = True)


    # Reorder them from most expensive to least expensive based
    # on the original prices:
    for bundle in bundle_offers_dict:
        bundle['items'] = sorted(bundle['items'], 
                                 key = lambda x: prices_dict[x],
                                 reverse = True
                                 )

    # Count items in basket and error if there are new items not present in LUTs
    basket = {}
    for sku in skus:
        if not sku in prices_dict:
            return -1
        basket[sku] = basket.get(sku, 0) + 1

    # The logic implies that getting one free in cross sales is always the best for the consumer
    # So you can do that first. To be modified if this commercial logic changes:
    for sku, values in get_free_products_offers_dict.items():
        # Calculate how many you need to remove from basket
        # (with a minimum of zero)
        if sku in basket:
            if values['target_sku_sale'] in basket:
                remove_from_basket = (basket[sku] // values['quantity']) \
                    * values['target_sku_reduction_quantity']
                basket[values['target_sku_sale']] = max(basket[values['target_sku_sale']] - remove_from_basket, 
                                                        0)

    # Check if any of the items in the basket has a special offer and compute
    # the offers first, sum the remainders. 
    # Otherwise just add the standard item * price
    final_checkout_basket = {}
    total_checkout_payment = 0
    # Create additional logic for bundle offers:
    for bundle in bundle_offers_dict:
        bundle_counter = {'total': 0}
        # Count each item into a total
        for sku in bundle['items']:
            if sku in basket:
                bundle_counter[sku] = basket[sku]
                bundle_counter['total'] += bundle_counter[sku]
                
        # Compute total number of bundles and delete items in order of price
        # (note that items have been ordered by their individual price to maximize
        # consumer savings)
        n_bundles = bundle_counter['total'] // bundle['quantity']
        individual_items_to_delete = n_bundles * bundle['quantity']

        # Update SKUs from bundle items in the main basket to compute remaining
        # individual prices in the following loop
        for sku in bundle['items']:
            if sku in basket: 
                bundle_counter[sku] = max(bundle_counter[sku] - individual_items_to_delete, 
                                          0)
                basket[sku] = bundle_counter[sku] # Update original basket
        total_checkout_payment += n_bundles * bundle['total_price']

    for sku, count in basket.items():
        payment = 0
        if sku in special_offers_dict:
            instrumental_count = count
            for offer_volume in special_offers_dict[sku]:
                if instrumental_count != 0:
                    total_packs = instrumental_count // offer_volume['quantity']    
                    payment += total_packs * offer_volume['total_price']
                    remainder = instrumental_count % offer_volume['quantity'] 
                    instrumental_count = remainder #readability
                
            payment += instrumental_count * prices_dict[sku]
            
        else: 
            payment = count * prices_dict[sku]
        
        final_checkout_basket[sku] = {'items': count, 'payment': payment}
        total_checkout_payment += payment
            
    # Apply cross sales in case they exist: 

    return total_checkout_payment
