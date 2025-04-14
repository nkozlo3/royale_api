async function fillInSuggestions(query, amount) {
  try {
    query += amount;
    const response = await fetch(
      `/search/fetch-meta-decks?query=${encodeURIComponent(query)}`
    );
    if (!response.ok) {
      throw new Error(
        "That didn't work. Please try again or use different cards and make sure you don't have spelling mistakes."
      );
    }
    const data = await response.json();
    const update_needed = data.update_needed;
    if (update_needed === "URGENT") {
      const ret = `<p>${data.message}</p>`;
      await fetch("/search/update-meta-decks", { method: "POST" });
      return ret;
    }
    if (update_needed === "BAD_USER_INPUT") {
      const ret = `<p>${data.message}</p>`;
      return ret;
    }
    let html = "";

    Object.keys(data.decks).forEach((deckName, index) => {
      const deck = data.decks[deckName];
      if (index % 4 === 0) {
        // new row
        if (index !== 0) {
          html += `</div>`;
        }
        html += `<div class="deck-row">`;
      }

      html += `
          <a
          class="deck-link"
          target="_blank"
          href="https://link.clashroyale.com/en/?clashroyale://copyDeck?deck=${deck.card1.id};${deck.card2.id};${deck.card3.id};${deck.card4.id};${deck.card5.id};${deck.card6.id};${deck.card7.id};${deck.card8.id}&tt=${deck.card1.tower_troop}&l=Royals"
        >
          <div class="deck">
          <div id="tower-troop" alt="${deck.card1.tower_troop}"></div>
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
          </div>
        </a>`;
    });

    if (Object.keys(data.decks).length % 4 !== 0) {
      html += `</div>`;
    }

    if (update_needed === true) {
      console.log(
        "Update required. Come back in 10 minutes for more meta decks."
      );
      await fetch("/search/update-meta-decks", { method: "POST" });
    }
    return html;
  } catch (error) {
    return `<p>Error: ${error.message}</p>`;
  }
}

window.fillInSuggestions = fillInSuggestions;
