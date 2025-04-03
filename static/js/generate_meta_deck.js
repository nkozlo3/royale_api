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
      display.innerHTML = `<a class=deck-link target= "_blank" href="https://link.clashroyale.com/deck/en?deck=${deck.card1.id};${deck.card2.id};${deck.card3.id};${deck.card4.id};${deck.card5.id};${deck.card6.id};${deck.card7.id};${deck.card8.id}">
      <div class="picture-row" id="picture-row">
      <img src="${deck.card1.picture_url}" alt="${deck.card1.name}" />
        <img src="${deck.card2.picture_url}" alt="${deck.card2.name}" />
        <img src="${deck.card3.picture_url}" alt="${deck.card3.name}" />
        <img src="${deck.card4.picture_url}" alt="${deck.card4.name}" />
      </div> 
      <div class="picture-row" id="picture-row">
        <img src="${deck.card5.picture_url}" alt="${deck.card5.name}" />
        <img src="${deck.card6.picture_url}" alt="${deck.card6.name}" />
        <img src="${deck.card7.picture_url}" alt="${deck.card7.name}" />
        <img src="${deck.card8.picture_url}" alt="${deck.card8.name}" />
      </div>
      </a>`;
      if (update_needed === true) {
        console.log(
          "Update required. Come back in 10 minutes for more meta decks."
        );
        await fetch("/search/update-meta-decks", { method: "POST" });
      }
    } catch (error) {
      display.innerHTML = `<p>Error: ${error.message}</p>`;
    }
  });
});
