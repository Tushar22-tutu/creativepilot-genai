# backend/test_brand_analysis.py

from brand_intelligence.analyzer import analyze_brand

brand_input = {
    "brand_name": "FitSphere",
    "product": "Online fitness coaching",
    "target_audience": "Working professionals",
    "tone": "premium"
}
brand_input["tone"] = "premium"


try:
    result = analyze_brand(brand_input)
    print("✅ Brand Analysis Successful:")
    print(result)
except Exception as e:
    print("❌ Brand Analysis Failed:")
    print(e)
