def calculate_total_price(items):
    total = 0
    for item in items:
        if item['type'] == 'book':
            total += item['price'] * 0.9 # 10% discount for books
        elif item['type'] == 'electronics':
            total += item['price'] * 0.8 # 20% discount for electronics
        else:
            total += item['price']
    return total 