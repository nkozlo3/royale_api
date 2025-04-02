document.addEventListener("DOMContentLoaded", function () {
  const link = document.createElement("link");

  const button = document.getElementById("generate-unique");
  const display = document.getElementById("deck-div");

  button.addEventListener("click", async () => {
    try {
      const response = await fetch("/generate/generate-deck");
      if (!response.ok) {
        throw new Error("That didn't work. Please try again.");
      }
      const data = await response.json();
      const deck = data.deck;
      console.log(deck);
      display.innerHTML = `<a class=deck-link target= "_blank" href="https://link.clashroyale.com/deck/en?deck=${deck.main_condition.id};${deck.win_condition.id};${deck.damage1.id};${deck.damage2.id};${deck.defense1.id};${deck.defense2.id};${deck.small_spell.id};${deck.spell.id}">
      <div class="picture-row" id="picture-row">
        <img src="${deck.main_condition.picture_url}" alt="${deck.main_condition.name}" />
        <img src="${deck.win_condition.picture_url}" alt="${deck.win_condition.name}" />
        <img src="${deck.damage1.picture_url}" alt="${deck.damage1.name}" />
        <img src="${deck.damage2.picture_url}" alt="${deck.damage2.name}" />
      </div>
      <div class="picture-row" id="picture-row">
        <img src="${deck.defense1.picture_url}" alt="${deck.defense1.name}" />
        <img src="${deck.defense2.picture_url}" alt="${deck.defense2.name}" />
        <img src="${deck.spell.picture_url}" alt="${deck.spell.name}" />
        <img src="${deck.small_spell.picture_url}" alt="${deck.small_spell.name}" />
      </div>
      </a>
      `;
    } catch (error) {
      display.innerHTML = `<p>Error:  ${error.message}</p>`;
    }
  });
});
