
function getPlaceIdFromURL() {
    const params = new URLSearchParams(
        window.location.search
    );

    return params.get("id");
}


async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            "Content-Type": "application/json"
        };

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(
            `${API_URL}/places/${placeId}`,
            {
                method: "GET",
                headers: headers
            }
        );

        if (!response.ok) {
            throw new Error("Place not found");
        }

        const place = await response.json();

        displayPlaceDetails(place);

    } catch (error) {
        console.error("Error:", error);

        const container =
            document.getElementById("place-details");

        if (container) {
            container.innerHTML = `
                <p class="error-message">
                    Unable to load place details.
                </p>
            `;
        }
    }
}


function displayPlaceDetails(place) {
    const container =
        document.getElementById("place-details");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const title = document.createElement("h1");
    title.textContent =
        place.title || "Unnamed place";

    const information = document.createElement("div");
    information.classList.add("place-info");

    const host = document.createElement("p");
    host.innerHTML = `
        <strong>Host:</strong>
        ${getHostName(place)}
    `;

    const price = document.createElement("p");
    price.innerHTML = `
        <strong>Price:</strong>
        $${place.price} per night
    `;

    const description = document.createElement("p");
    description.innerHTML = `
        <strong>Description:</strong>
        ${place.description || "No description available."}
    `;

    information.appendChild(host);
    information.appendChild(price);
    information.appendChild(description);

    const amenitiesTitle =
        document.createElement("h2");

    amenitiesTitle.textContent = "Amenities";

    const amenitiesList =
        document.createElement("ul");

    const amenities =
        place.amenities || [];

    if (amenities.length === 0) {
        const emptyItem =
            document.createElement("li");

        emptyItem.textContent =
            "No amenities available.";

        amenitiesList.appendChild(emptyItem);

    } else {
        amenities.forEach((amenity) => {
            const item =
                document.createElement("li");

            if (typeof amenity === "string") {
                item.textContent = amenity;
            } else {
                item.textContent =
                    amenity.name || "Unknown amenity";
            }

            amenitiesList.appendChild(item);
        });
    }

    information.appendChild(amenitiesTitle);
    information.appendChild(amenitiesList);

    container.appendChild(title);
    container.appendChild(information);

    displayReviews(place.reviews || []);
}


function getHostName(place) {
    if (!place.owner) {
        return "Unknown";
    }

    const firstName =
        place.owner.first_name || "";

    const lastName =
        place.owner.last_name || "";

    const fullName =
        `${firstName} ${lastName}`.trim();

    return fullName || "Unknown";
}


function displayReviews(reviews) {
    const container =
        document.getElementById("place-details");

    if (!container) {
        return;
    }

    const reviewsTitle =
        document.createElement("h2");

    reviewsTitle.textContent = "Reviews";

    container.appendChild(reviewsTitle);

    if (reviews.length === 0) {
        const message =
            document.createElement("p");

        message.textContent =
            "No reviews yet.";

        container.appendChild(message);

        return;
    }

    reviews.forEach((review) => {
        const card =
            document.createElement("article");

        card.classList.add("review-card");

        const user =
            document.createElement("h3");

        user.textContent =
            getReviewUser(review);

        const rating =
            document.createElement("p");

        rating.classList.add("rating");

        rating.textContent =
            `Rating: ${review.rating}/5`;

        const comment =
            document.createElement("p");

        comment.textContent =
            review.comment || "No comment.";

        card.appendChild(user);
        card.appendChild(rating);
        card.appendChild(comment);

        container.appendChild(card);
    });
}


function getReviewUser(review) {
    if (!review.user) {
        return "Anonymous";
    }

    const first =
        review.user.first_name || "";

    const last =
        review.user.last_name || "";

    const name =
        `${first} ${last}`.trim();

    return name || "Anonymous";
}


function setupPlacePage() {
    const details =
        document.getElementById("place-details");

    if (!details) {
        return;
    }

    const placeId =
        getPlaceIdFromURL();

    if (!placeId) {
        details.innerHTML = `
            <p class="error-message">
                Place ID is missing.
            </p>
        `;

        return;
    }

    const token = getCookie("token");

    const loginLink =
        document.getElementById("login-link");

    const reviewSection =
        document.getElementById("add-review");

    if (token) {
        if (loginLink) {
            loginLink.style.display = "none";
        }

        if (reviewSection) {
            reviewSection.style.display = "block";
        }
    } else {
        if (loginLink) {
            loginLink.style.display = "block";
        }

        if (reviewSection) {
            reviewSection.style.display = "none";
        }
    }

    fetchPlaceDetails(token, placeId);
}
 id="b5v8ko"
async function submitReview(
    token,
    placeId,
    reviewText,
    rating
) {
    const response = await fetch(
        `${API_URL}/reviews/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({
                text: reviewText,
                rating: Number(rating),
                place_id: placeId
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.error || "Failed to submit review"
        );
    }

    return data;
}


function setupReviewForm() {
    const reviewForm =
        document.getElementById("review-form");

    if (!reviewForm) {
        return;
    }

    const token = getCookie("token");

    /*
     * The review page is available
     * only for authenticated users.
     */
    if (!token) {
        window.location.href = "index.html";
        return;
    }

    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        window.location.href = "index.html";
        return;
    }

    reviewForm.addEventListener(
        "submit",
        async (event) => {
            event.preventDefault();

            const comment =
                document.getElementById("comment").value.trim();

            const rating =
                document.getElementById("rating").value;

            const message =
                document.getElementById("review-message");

            if (message) {
                message.textContent = "";
            }

            if (!comment || !rating) {
                if (message) {
                    message.textContent =
                        "Please complete all fields.";
                }

                return;
            }

            try {
                await submitReview(
                    token,
                    placeId,
                    comment,
                    rating
                );

                if (message) {
                    message.textContent =
                        "Review submitted successfully!";

                    message.style.color = "green";
                }

                reviewForm.reset();

            } catch (error) {
                console.error(error);

                if (message) {
                    message.textContent =
                        error.message;

                    message.style.color = "#d32f2f";
                }
            }
        }
    );
}



