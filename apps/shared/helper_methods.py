def discount(price, discount):
    checkout_price = price
    if discount != 0:
        checkout_price =  price - price * discount/100
    return checkout_price
