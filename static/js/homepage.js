

document.getElementById("profileBtn").addEventListener("click", function() {
    // Redirect to the profile page
    window.location.href = "/cv"; // Replace with the actual profile page URL
});

document.getElementById("profile_userBtn").addEventListener("click", function() {
    var searchedUserId = this.getAttribute("data-user-id");
    // Redirect to the profile page
    window.location.href = `/cv?searched_user_id=${searchedUserId}`;
});

document.getElementById("updateBtn").addEventListener("click", function() {
    // Redirect to the cv form page
    window.location.href = "/cv_form"; // Replace with the actual profile page URL
});

document.getElementById("newPostBtn").addEventListener("click", function() {
    // Redirect to the create new post page
    window.location.href = "/create-post"; // Replace with the actual create post page URL
});



// Hide suggestions when clicking outside
document.addEventListener('click', function(event) {
    const suggestions = document.getElementById('suggestions');
    if (!event.target.closest('#search-form')) {
        suggestions.style.display = 'none';
    }
});

let slideIndex = 1;
showSlides(slideIndex);

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.querySelectorAll(".slide");
    let dots = document.querySelectorAll(".dot");

    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}

setInterval(() => {
    showSlides(++slideIndex);
}, 5000); // Change slide every 5 seconds

function searchUsers(query) {
    if (query.length < 2) {
        document.getElementById('suggestions').style.display = 'none';
        return;
    }
    fetch(`/search_suggestions?query=${query}`)
        .then(response => response.json())
        .then(data => {
            let suggestions = document.getElementById('suggestions');
            suggestions.innerHTML = '';  // Clear previous suggestions
            if (data.length > 0) {
                data.forEach(user => {
                    let suggestion = document.createElement('div');
                    suggestion.innerHTML = user.username;
                    suggestion.onclick = function() { loadUserDashboard(user.id); };
                    suggestions.appendChild(suggestion);
                });
                suggestions.style.display = 'block';  // Show suggestions
            } else {
                suggestions.style.display = 'none';  // Hide if no results
            }
        });
}

function loadUserDashboard(searchedUserId) {
    window.location.href = `/dashboard?searched_user_id=${searchedUserId}`;
}

