def calculate_roi(cost_price):
    """
    מקבל מחיר עלות (cost_price),
    מחזיר מחיר מכירה מומלץ (פי 4) ו-ROI באחוזים.
    """
    sell_price = cost_price * 4
    roi = ((sell_price - cost_price) / cost_price) * 100
    return sell_price, roi
