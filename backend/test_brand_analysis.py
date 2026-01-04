from brand_intelligence.analyzer import analyze_brand

if __name__ == "__main__":
    brand_input = {
        "brand_name": "FitSphere",
        "product": "Online fitness coaching",
        "target_audience": "Working professionals",
        "tone": "premium"
    }

    result = analyze_brand(brand_input)
    print("Brand Analysis Result:")
    print(result)
