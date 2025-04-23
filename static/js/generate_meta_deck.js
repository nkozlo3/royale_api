document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("generate-meta");
  const display = document.getElementById("deck-div");
  const searchInput = document.getElementById("search-input");

  window.onload = function () {
    button.click();
  };

  searchInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      button.click();
    }
  });

  button.addEventListener("click", async () => {
    const query = searchInput.value.trim();
    const html = await window.fillInSuggestions(query, ",32");
    display.innerHTML = html;
  });
});
