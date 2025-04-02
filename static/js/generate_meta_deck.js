document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("generate-meta");
  const display = document.getElementById("deck-div");

  button.addEventListener("click", async () => {
    try {
      const response = await fetch("/search/fetch-meta-decks");
      if (!response.ok) {
        throw new Error("That didn't work. Please try again");
      }
      const data = await response.json();
      const update_needed = data.update_needed;
      if (update_needed === "URGENT") {
        display.innerHTML = `<p>${data.message}</p>`;
        await fetch("/search/update-meta-decks", { method: "POST" });
        return;
      }

      const deck = data.deck;
    } catch (error) {
      display.innerHTML = `<p>Error: ${error.message}</p>`;
    }
  });
});
