document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("generate-war-decks");
  const display = document.getElementById("war-decks-div");

  function generateInnerHTML(urls, ids) {
    let html = "";
    let link = "https://link.clashroyale.com/deck/en?deck=" + ids[0];
    for (let j = 1; j < ids.length; j++) {
      link += ";" + ids[j];
    }
    console.log(link);
    for (let i = 0; i < 4; i++) {
      if (i === 0) {
        html += `<div class="deck-row">`;
      }
      html += `
          <div class="deck">
            <div class="picture-row" id="picture-row">
              <img
                class="empty-card"
                src="${urls[0]}"
                alt="deck${i + 1}-card1"
              />
              <img
                class="empty-card"
                src="${urls[1]}"
                alt="deck${i + 1}-card2"
              />
              <img
                class="empty-card"
                src="${urls[2]}"
                alt="deck${i + 1}-card3"
              />
              <img
                class="empty-card"
                src="${urls[3]}"
                alt="deck${i + 1}-card4"
              />
            </div>
            <div class="picture-row" id="picture-row">
              <img
                class="empty-card"
                src="${urls[4]}"
                alt="deck${i + 1}-card5"
              />
              <img
                class="empty-card"
                src="${urls[5]}"
                alt="deck${i + 1}-card6"
              />
              <img
                class="empty-card"
                src="${urls[6]}"
                alt="deck${i + 1}-card7"
              />
              <img
                class="empty-card"
                src="${urls[7]}"
                alt="deck${i + 1}-card8"
              />
            </div>
          </div>
      `;
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
    display.innerHTML = generateInnerHTML(urls, ids);
  };
});
