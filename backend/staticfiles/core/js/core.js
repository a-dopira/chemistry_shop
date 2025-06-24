document.addEventListener("click", function (e) {
    const searchResults = document.getElementById("search-results");
    const searchForm = document.querySelector(".form_search");
    if (!searchForm.contains(e.target)) {
        searchResults.style.display = "none";
    }
});

document.body.addEventListener("htmx:afterSwap", function (e) {
    if (e.target.id === "search-results") {
        const results = e.target;
        results.style.display = results.innerHTML.trim() ? "block" : "none";
    }
});