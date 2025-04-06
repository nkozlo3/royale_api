document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("generate-war-decks");
  const display = document.getElementById("war-decks-div");
  const main_war_decks = document.getElementById("main-war-decks");
  const select_card = document.getElementById("select-card");
  const cancel = document.getElementById("cancel-card-button");
  let currCardId = "";
  const cardsSet = new Set();

  const cards_display = document.getElementById("cards-display");

  const card_type_buttons = ["common", "rare", "epic", "legendary", "champion"];

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
    bringBackMain();
  }

  function bringBackMain() {
    main_war_decks.style.display = "block";
    select_card.style.display = "none";
  }

  cancel.addEventListener("click", async () => {
    bringBackMain();
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
      html += `<div class="deck">`;
      for (let j = 0; j < 8; j++) {
        if (j === 0 || j === 4) {
          html += `<div class="picture-row" id="picture-row">`;
        }
        html += `
        <img
          class="empty-card"
          onclick="removeMainSelectCard('deck${i + 1}-card${j + 1}')"
          src="${urls[0]}"
          alt="deck${i + 1}-card${j + 1}"
          id="deck${i + 1}-card${j + 1}"
        />
        `;
        if (j === 3 || j == 7) {
          html += `</div>`;
        }
      }
      html += `</div>`; // closes <div class = "deck">
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
  };
});
