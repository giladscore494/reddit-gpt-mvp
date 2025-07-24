def calculate_roi(cost_price):
    sell_price = cost_price * 4
    roi = ((sell_price - cost_price) / cost_price) * 100
    return sell_price, roi
