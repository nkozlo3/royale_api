import { alphaFiltering, setAlphaFiltering} from "./alpha_filter.js";

document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("generate-meta");
  const display = document.getElementById("deck-div");
  const searchInput = document.getElementById("search-input");

  window.onload = function () {
    setAlphaFiltering(0);
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
    console.log(query);
    const html = await window.fillInSuggestions(query, ",32", alphaFiltering);
    display.innerHTML = html;
  });
});
