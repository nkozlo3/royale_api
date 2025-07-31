document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("generate-meta");
  const display = document.getElementById("deck-div");
  const searchInput = document.getElementById("search-input");
  const alphaFilter = document.getElementById("filter-alpha-button");
  let alphaFiltering = 0;

  window.onload = function () {
    button.click();
  };

  searchInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      button.click();
    }
  });

  alphaFilter.addEventListener("click", async () => {
    if (alphaFilter.textContent === "Alpha filter?") {
      alphaFilter.textContent = "Alpha filtering";
      alphaFiltering = 1;
    } else {
      alphaFilter.textContent = "Alpha filter?";
      alphaFiltering = 0;
    }
  });

  button.addEventListener("click", async () => {
    const query = searchInput.value.trim();
    console.log(query);
    const html = await window.fillInSuggestions(query, ",32", alphaFiltering);
    display.innerHTML = html;
  });
});
