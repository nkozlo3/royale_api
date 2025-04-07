document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("generate-war-decks");
  const cancel = document.getElementById("cancel-card-button");
  const clear_slot = document.getElementById("remove-slot");
  const searchInput = document.getElementById("search-input");

  const display = document.getElementById("war-decks-div");
  const main_war_decks = document.getElementById("main-war-decks");
  const select_card = document.getElementById("select-card");
  let currCardId = "";
  const cardsSet = new Set();

  const cards_display = document.getElementById("cards-display");
  const war_decks_suggestions_display = document.getElementById(
    "war-decks-suggestions"
  );

  const card_type_buttons = ["common", "rare", "epic", "legendary", "champion"];
  const deck_input_ids = [
    "search-input-deck1",
    "search-input-deck2",
    "search-input-deck3",
    "search-input-deck4",
  ];
  for (const card_type of card_type_buttons) {
    let curr_id = card_type + "-button";
    const element = document.getElementById(curr_id);

    element.addEventListener("click", async () => {
      displayAndEnableCards(card_type);
    });
  }

  async function displayAndEnableCards(card_type) {
    cards_display.innerHTML = "";
    const response = await fetch(
      `/helpers/cards-by-rarity?query=${encodeURIComponent(card_type)}`
    );
    if (!response.ok) {
      throw new Error("Hrmm. Try again please");
    }
    const data = await response.json();

    const cards = data.cards;
    let card_html = `<div class="picture-row id="picture-row">`;

    Object.entries(cards).forEach(([cardName, card]) => {
      card_html += `<img onclick="bringBackMainAndSetUpCard('${card.picture_url}', '${cardName}')" src="${card.picture_url}" alt="${cardName}" />`;
    });
    card_html += `</div>`;
    cards_display.innerHTML = card_html;
  }

  async function removeMainSelectCard(buttonId) {
    const temp = document.getElementById(buttonId).alt;
    cardsSet.delete(temp);
    main_war_decks.style.display = "none";
    select_card.style.display = "block";
    currCardId = buttonId;
  }

  async function bringBackMainAndSetUpCard(src, cardName) {
    currCard = document.getElementById(currCardId);
    currCard.src = src;
    currCard.alt = cardName;
    cardsSet.add("!" + cardName);
    let addToStorage = cardName + "," + src;
    localStorage.setItem(currCardId, addToStorage);
    bringBackMain();
  }

  function bringBackMain() {
    main_war_decks.style.display = "block";
    select_card.style.display = "none";
  }

  cancel.addEventListener("click", async () => {
    bringBackMain();
  });
  clear_slot.addEventListener("click", async () => {
    localStorage.removeItem(currCardId);
    bringBackMain();
    window.location.reload();
  });

  window.removeMainSelectCard = removeMainSelectCard;
  window.bringBackMainAndSetUpCard = bringBackMainAndSetUpCard;

  function generateInnerHTML(urls, ids) {
    let html = "";
    let link = "https://link.clashroyale.com/deck/en?deck=" + ids[0];
    for (let j = 1; j < ids.length; j++) {
      link += ";" + ids[j];
    }
    for (let i = 0; i < 4; i++) {
      if (i === 0) {
        html += `<div class="deck-row">`;
      }
      html += `<div class="deck-input-wrapper">
                <input
                  type="text"
                  id="search-input-deck${i + 1}"
                  placeholder="Optionally enter card names (comma-seperated)"
                />`;
      html += `<div id="deck${i + 1}" class="deck">`;
      for (let j = 0; j < 8; j++) {
        let currItem = `deck${i + 1}-card${j + 1}`;
        const potential = localStorage.getItem(currItem);
        let src = `${urls[0]}`;
        if (potential !== null) {
          const items = potential.split(",");
          cardsSet.add("!" + items[0]);
          src = items[1];
        }
        if (j === 0 || j === 4) {
          html += `<div class="picture-row" id="picture-row">`;
        }
        html += `
        <img
          class="empty-card"
          onclick="removeMainSelectCard('${currItem}')"
          src="${src}"
          alt="${currItem}"
          id="${currItem}"
        />
        `;
        if (j === 3 || j == 7) {
          html += `</div>`;
        }
      }
      html += `</div>`; // closes <div class="deck">
      html += `</div>`; // closes <div class="deck-input-wrapper">
      if (i === 3) {
        html += `</div>`;
      }
    }
    return html;
  }

  window.onload = function () {
    urls = [
      "../static/images/blank_slot.png",
      "../static/images/blank_slot.png",
      "../static/images/blank_slot.png",
      "../static/images/blank_slot.png",
      "../static/images/blank_slot.png",
      "../static/images/blank_slot.png",
      "../static/images/blank_slot.png",
      "../static/images/blank_slot.png",
    ];
    ids = [
      "00000000",
      "00000000",
      "00000000",
      "00000000",
      "00000000",
      "00000000",
      "00000000",
      "00000000",
    ];
    html = generateInnerHTML(urls, ids);
    display.innerHTML = html;

    for (const deck_input of deck_input_ids) {
      const element = document.getElementById(deck_input);
      element.addEventListener("keydown", async function (event) {
        console.log(element);
        if (event.key === "Enter") {
          event.preventDefault();
          const currDeckId = element.id.split("-").pop();
          const currDeck = await document.getElementById(currDeckId);
          let query = "";
          cardsSet.forEach((card) => {
            query += card + ",";
          });
          const wanted_cards = element.value.trim();
          query += wanted_cards;
          console.log(query);
          const deck_in_html = await window.fillInSuggestions(query, ",1");
          const parser = new DOMParser();
          const doc = parser.parseFromString(deck_in_html, "text/html");
          const linkElement = doc.querySelector("a.deck-link");
          const href = linkElement ? linkElement.href : null;

          const images = doc.querySelectorAll("img");
          const imageSrcs = Array.from(images).map((img) => img.src);

          for (imageSrc of imageSrcs) {
            console.log(imageSrcs[0]);
          }
        }
      });
    }
  };

  searchInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      button.click();
    }
  });

  button.addEventListener("click", async () => {
    let query = "";
    cardsSet.forEach((element) => {
      query += element + ",";
    });
    const wanted_cards = searchInput.value.trim();
    query += wanted_cards;
    war_decks_suggestions_display.innerHTML = await window.fillInSuggestions(
      query,
      ",8"
    );
  });
});
