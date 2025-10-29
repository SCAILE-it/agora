"""Shopping tools for product search (mock implementation for MVP)."""

def search_amazon(query: str) -> str:
    """
    Mock Amazon product search.

    In production, this would integrate with actual shopping APIs.
    For MVP, returns placeholder data.
    """
    mock_products = [
        {
            "name": f"{query} - Premium Model",
            "price": "$199.99",
            "rating": "4.5/5",
            "features": "High quality, fast shipping, top-rated"
        },
        {
            "name": f"{query} - Budget Option",
            "price": "$79.99",
            "rating": "4.0/5",
            "features": "Good value, reliable, popular choice"
        },
        {
            "name": f"{query} - Professional Grade",
            "price": "$349.99",
            "rating": "4.8/5",
            "features": "Premium build, warranty included, best seller"
        }
    ]

    result = f"Top 3 results for '{query}':\n\n"
    for i, product in enumerate(mock_products, 1):
        result += f"{i}. {product['name']}\n"
        result += f"   Price: {product['price']}\n"
        result += f"   Rating: {product['rating']}\n"
        result += f"   Features: {product['features']}\n\n"

    return result
