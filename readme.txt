1. Create error/warning if incorrect data has been input to create_listing page, resulting in no entry to db

2. Save categories in models.py instead of a line in top of views.py. This should also fix category-unusuality in the create_listing function

{% block body %}
    <h2>Active Listings</h2>

    <div>
        <ul>
            {% for listing in auction_listings %}
                <li>
                    Listing title: {{ listing.title }}. {{ listing.description }}. The price is {{ listing.price }}.
                    <br>Posted {{ listing.date_of_post }}
                </li>
                    {% if listing.url_picture %}
                        <img src="{{ listing.url_picture }}" alt="Listing Picture">
                    {% endif %}
                    <div>Category: {{ listing.get_category_display }}</div>
            {% empty %}
                <li>No listings</li>
            {% endfor %}
        </ul>
    </div>
{% endblock %}