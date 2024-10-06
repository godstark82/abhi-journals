from flask import jsonify
from db_instance import get_db

def get_social_links():
    # Get the database instance
    db = get_db()

    # Fetch social links from Firestore
    social_links_ref = db.collection('socialLinks')
    social_links = social_links_ref.stream()

    # Extract name and url from each document
    social_links_data = [
        {
            'url': link.to_dict().get('url', '#')
        } for link in social_links
    ]

    # Return the data as JSON
    return jsonify(social_links_data)