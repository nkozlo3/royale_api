export let alphaFiltering = 0;

export function setAlphaFiltering(value) {
    alphaFiltering = value;
}

document.addEventListener("DOMContentLoaded", function () {
    const alphaFilter = document.getElementById("filter-alpha-button");

  alphaFilter.addEventListener("click", async () => {
    if (alphaFilter.textContent === "Alpha filter?") {
        alphaFilter.textContent = "Alpha filtering";
        alphaFiltering = 1;
    } else {
        alphaFilter.textContent = "Alpha filter?";
        alphaFiltering = 0;
    }
  });
});