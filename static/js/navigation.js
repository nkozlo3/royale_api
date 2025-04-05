document.addEventListener("DOMContentLoaded", function () {
  function addNavigation(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
      const url = button.getAttribute("data-url");
      button.addEventListener("click", function () {
        window.location.href = url;
      });
    }
  }

  addNavigation("search-page");
  addNavigation("war_decks-page");
  addNavigation("main-page");
});
