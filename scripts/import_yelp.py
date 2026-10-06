import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
YELP_DIR = ROOT / "data" / "raw" / "yelp"

BUSINESS_FILE = YELP_DIR / "yelp_academic_dataset_business.json"
REVIEW_FILE = YELP_DIR / "yelp_academic_dataset_review.json"
OUTPUT_FILE = ROOT / "data" / "raw" / "services_raw.csv"

CATEGORY_MAP = {
    "health & medical": "Healthcare",
    "health and medical": "Healthcare",
    "medical centers": "Healthcare",
    "doctors": "Healthcare",
    "dentists": "Healthcare",
    "hospitals": "Healthcare",
    "beauty & spas": "Beauty & Wellness",
    "beauty and spas": "Beauty & Wellness",
    "hair salons": "Beauty & Wellness",
    "nail salons": "Beauty & Wellness",
    "spas": "Beauty & Wellness",
    "home services": "Domestic Services",
    "cleaning": "Domestic Services",
    "plumbing": "Domestic Services",
    "electricians": "Domestic Services",
    "handyman": "Domestic Services",
    "education": "Education Support",
    "tutoring centers": "Education Support",
    "specialty schools": "Education Support",
    "preschools": "Education Support",
    "transportation": "Transport",
    "taxis": "Transport",
    "public transportation": "Transport",
    "car rental": "Transport",
    "airport shuttles": "Transport",
}

def normalise_text(value):
    if value is None:
        return ""
    value = str(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()

def find_wasaa_category(categories):
    if not categories:
        return None
    categories = [
        normalise_text(category).lower()
        for category in categories.split(",")
    ]
    for category in categories:
        if category in CATEGORY_MAP:
            return CATEGORY_MAP[category]
    return None

def load_businesses():
    businesses = []
    with open(BUSINESS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            businesses.append(json.loads(line))
    return businesses

def main():
    print("Loading Yelp business data...")
    businesses = load_businesses()
    print(f"Loaded {len(businesses):,} businesses.")

    print("Selecting businesses relevant to WaSaa...")
    selected = []
    active_business_ids = set()

    for business in businesses:
        category = find_wasaa_category(business.get("categories"))
        if category is None:
            continue

        b_id = business.get("business_id")
        active_business_ids.add(b_id)

        selected.append({
            "business_id": b_id,
            "provider_name": normalise_text(business.get("name")),
            "category": category,
            "city": normalise_text(business.get("city")),
            "area": normalise_text(business.get("neighborhood") or business.get("address") or business.get("city")),
            "rating_avg": business.get("stars"),
            "review_count": business.get("review_count"),
            "categories": normalise_text(business.get("categories")),
            "attributes": business.get("attributes"),
            "hours": business.get("hours"),
        })

    print(f"Selected {len(selected):,} relevant businesses.")
    print("Loading and filtering reviews safely...")

    review_lookup = {}
    
    # Reads the 4.5GB file row-by-row into memory instead of all at once
    with open(REVIEW_FILE, "r", encoding="utf-8") as file:
        for line in file:
            review = json.loads(line)
            b_id = review.get("business_id")
            
            # Skip if this review belongs to an out-of-scope business
            if b_id not in active_business_ids:
                continue
                
            if b_id not in review_lookup:
                review_lookup[b_id] = []
                
            # Cap at 3 reviews per business to prevent massive RAM bloat
            if len(review_lookup[b_id]) < 3:
                text = normalise_text(review.get("text"))
                if text:
                    review_lookup[b_id].append(text)

    records = []
    for business in selected:
        business_id = business["business_id"]
        reviews_for_business = review_lookup.get(business_id, [])
        review_text = " ".join(reviews_for_business[:3])

        description_parts = [
            f"{business['provider_name']} provides {business['category'].lower()} services."
        ]
        if business["categories"]:
            description_parts.append(f"Business categories include {business['categories']}.")
        if review_text:
            description_parts.append(f"Customer feedback includes: {review_text[:800]}")

        description = " ".join(description_parts)

        records.append({
            "provider_name": business["provider_name"],
            "service_name": f"{business['category']} services",
            "category": business["category"],
            "description": description,
            "keywords": business["categories"],
            "area": business["area"],
            "city": business["city"],
            "price_min": None,
            "price_max": None,
            "rating_avg": business["rating_avg"],
            "review_count": business["review_count"],
            "availability_days": None,
            "data_origin": "public",
        })

    dataframe = pd.DataFrame(records)
    dataframe = dataframe.drop_duplicates(subset=["provider_name", "service_name"])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(OUTPUT_FILE, index=False)

    print()
    print("SUCCESS")
    print(f"Created {len(dataframe):,} service records.")
    print(f"Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
