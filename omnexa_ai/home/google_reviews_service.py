"""
Google Business Reviews / Google Places API integration.

Uses the Google Places API (New) to fetch reviews for a business.
Requires a Google Cloud API key with Places API enabled.

To get a Place ID: https://developers.google.com/maps/documentation/places/web-service/place-id
To get an API key: https://developers.google.com/maps/documentation/places/web-service/get-api-key
"""

import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

GOOGLE_PLACES_API_BASE = "https://places.googleapis.com/v1/places"


def fetch_google_reviews(place_id, api_key):
    """Fetch reviews from Google Places API (New)."""
    if not place_id or not api_key:
        logger.warning("Google reviews fetch skipped: place_id or api_key not configured")
        return []

    url = f"{GOOGLE_PLACES_API_BASE}/{place_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "reviews,displayName",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error(f"Failed to fetch Google reviews: {exc}")
        return []

    data = response.json()

    if "reviews" not in data:
        logger.warning(f"No reviews found or invalid response")
        return []

    reviews = []
    for review in data.get("reviews", []):
        review_data = {
            "author_name": review.get("authorAttribution", {}).get("displayName", "Anonymous"),
            "rating": review.get("rating", 0),
            "text": review.get("text", {}).get("text", "") if review.get("text") else "",
            "time": review.get("publishTime", ""),
            "review_id": review.get("name", ""),
            "relative_time": review.get("relativePublishTimeDescription", ""),
        }
        reviews.append(review_data)

    logger.info(f"Fetched {len(reviews)} reviews from Google")
    return reviews


def sync_google_reviews_to_testimonials(config, max_reviews=50):
    """Fetch Google reviews and sync them as Testimonial models."""
    from .models import Testimonial

    result = {"created": 0, "updated": 0, "skipped": 0, "errors": []}

    reviews = fetch_google_reviews(config.place_id, config.api_key)

    for review in reviews[:max_reviews]:
        try:
            review_date = None
            if review.get("time"):
                try:
                    review_date = datetime.fromisoformat(review["time"].replace("Z", "+00:00"))
                except ValueError:
                    pass

            review_id = review.get("review_id", "")

            existing = Testimonial.objects.filter(
                google_review_id=review_id,
                is_from_google=True
            ).first()

            if existing:
                existing.rating = review.get("rating", existing.rating)
                existing.quote = review.get("text", existing.quote)
                existing.save(update_fields=["rating", "quote", "updated_at"])
                result["updated"] += 1
            else:
                Testimonial.objects.create(
                    client_name=review.get("author_name", "Anonymous").strip(),
                    client_company="",
                    client_title="",
                    quote=review.get("text", ""),
                    rating=min(int(review.get("rating", 5)), 5),
                    is_from_google=True,
                    google_review_id=review_id,
                    google_star_rating=min(int(review.get("rating", 5)), 5),
                    google_review_date=review_date,
                    is_active=True,
                )
                result["created"] += 1

        except Exception as exc:
            result["errors"].append(str(exc))
            result["skipped"] += 1
            logger.error(f"Error syncing review: {exc}")

    return result
