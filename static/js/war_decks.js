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
  const copy_button_ids = [
    "deck1-copy-button",
    "deck2-copy-button",
    "deck3-copy-button",
    "deck4-copy-button",
  ];
  const clear_button_ids = [
    "deck1-clear-button",
    "deck2-clear-button",
    "deck3-clear-button",
    "deck4-clear-button",
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
      card_html += `<img onclick="bringBackMainAndSetUpCard('${card.picture_url}', '${cardName}${card.id}')" src="${card.picture_url}" alt="${cardName}" />`;
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

  async function saveCard(src, cardName, cardID) {
    const currCard = document.getElementById(cardID);
    currCard.src = src;
    currCard.alt = cardName;
    if (!cardsSet.has("!" + cardName)) {
      cardsSet.add("!" + cardName);
    }
    let addToStorage = cardName + "," + src;
    localStorage.setItem(cardID, addToStorage);
  }

  async function bringBackMainAndSetUpCard(src, cardName) {
    saveCard(src, cardName, currCardId);
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
    let link = "https://link.clashroyale.com/en/?clashroyale://copyDeck?deck=" + ids[0];
    for (let j = 1; j < ids.length; j++) {
      link += ";" + ids[j];
    }
    link += "&l=Royals";
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
        let alt = `${currItem}00000000`;
        if (potential !== null) {
          const items = potential.split(",");
          cardsSet.add("!" + items[0]);
          src = items[1];
          alt = items[0];
        }
        if (j === 0 || j === 4) {
          html += `<div class="picture-row" id="picture-row">`;
        }
        html += `
        <img
          class="empty-card"
          onclick="removeMainSelectCard('${currItem}')"
          src="${src}"
          alt="${alt}"
          id="${currItem}"
        />
        `;
        if (j === 3 || j == 7) {
          html += `</div>`;
        }
      }
      html += `<div id=deck${i + 1}-not-found></div>`;
      html += `</div>`; // closes <div class="deck">
      html += `
            <div class="deck-buttons">
              <button
                  class="bangers-regular cButton"
                  id="deck${i + 1}-copy-button"
                  style="padding: 0.5rem 1rem"
                  target="_blank"
                  href=""
                  type="button"
                >
                  Copy Deck
                </button>
              <button
                class="bangers-regular cButton"
                id="deck${i + 1}-clear-button"
                style="padding: 0.5rem 1rem"
                type="button"
              >
                Clear Deck
              </button>
            </div>`;
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
        if (event.key === "Enter") {
          event.preventDefault();

          const currDeckId = element.id.split("-").pop();
          const currDeck = await document.getElementById(currDeckId);
          let alts = [];

          errorDisp = document.getElementById(currDeckId + "-not-found");
          errorDisp.innerHTML = ``;

          for (row of currDeck.querySelectorAll(".picture-row")) {
            for (potential of row.querySelectorAll(".empty-card")) {
              potentialAlt = potential.getAttribute("alt");
              let originalName = potentialAlt.replace(/\d{8}$/, "");
              const checker = potentialAlt.substring(0, 4);
              if (checker !== "deck") {
                alts.push(originalName);
              }
            }
          }

          let query = "";
          cardsSet.forEach((card) => {
            const originalName = card.replace(/\d{8}$/, "");
            query += originalName + ",";
          });
          const wanted_cards = element.value.trim();
          query += wanted_cards;
          let queries = query.split(",");
          for (alt of alts) {
            let originalName = alt.replace(/\d{8}$/, "");
            const checker = "!" + originalName;
            queries = queries.filter((q) => q.trim() !== checker);
            queries.push(originalName);
          }

          query = queries.join(",");

          const deck_in_html = await window.fillInSuggestions(query, ",1");
          const parser = new DOMParser();
          const doc = parser.parseFromString(deck_in_html, "text/html");
          const linkElement = doc.querySelector("a.deck-link");
          if (linkElement === null) {
            console.log("THIS IS WORKINGISH");
            errorDisp.innerHTML = `<b style="color: red"> No decks available with these cards. </b>`;
            return;
          }
          const href = linkElement ? linkElement.href : null;
          let ids = href.split("=")[1].split(";");
          const images = doc.querySelectorAll("img");
          const imageSrcs = Array.from(images).map((img) => img.src);
          let names = Array.from(images).map((n) => n.alt);
          for (let index = 0; index < 8; index++) {
            names[index] += ids[index];
          }

          let i = 0;
          for (row of currDeck.querySelectorAll(".picture-row")) {
            for (card of row.querySelectorAll(".empty-card")) {
              saveCard(imageSrcs[i], names[i], card.getAttribute("id"));
              i += 1;
            }
          }
        }
      });
    }

    for (const copy_button_id of copy_button_ids) {
      copy_button = document.getElementById(copy_button_id);
      copy_button.addEventListener("click", async function (event) {
        const deck = document.getElementById(copy_button_id.substring(0, 5));
        let cards = [];
        let ids = [];
        for (row of deck.querySelectorAll(".picture-row")) {
          for (potential of row.querySelectorAll(".empty-card")) {
            const cardName = potential.getAttribute("alt");
            ids.push(cardName.slice(-8));
          }
        }

        event.preventDefault();
        window.open(
          `https://link.clashroyale.com/deck/en?deck=${ids[0]};${ids[1]};${ids[2]};${ids[3]};${ids[4]};${ids[5]};${ids[6]};${ids[7]}&l=Royals`,
          "_blank"
        );
      });
    }

    for (const clear_button_id of clear_button_ids) {
      clear_button = document.getElementById(clear_button_id);
      clear_button.addEventListener("click", async function (event) {
        const deck = document.getElementById(clear_button_id.substring(0, 5));

        for (row of deck.querySelectorAll(".picture-row")) {
          for (potential of row.querySelectorAll(".empty-card")) {
            const id = potential.getAttribute("id");
            localStorage.removeItem(id);
          }
        }
        window.location.reload();
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
