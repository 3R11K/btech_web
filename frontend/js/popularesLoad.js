document.addEventListener("DOMContentLoaded", function () {
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", "/api/populares", true);
    xmlhttp.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        let response = JSON.parse(this.responseText);
        let populares = document.getElementById("popularesCards");
        for (key in response) {
          let name = response[key];
          populares.innerHTML += `<div class="card">
                                      <img src="../images/courseImage.png" alt="${name}" id="imageCard">
                                      <h3 class="name">${name}</h3>
                                  </div>`;
        }
  
        // A variável container agora é definida no escopo externo
        const container = document.getElementById("popularesCards");
        const cards = document.querySelectorAll(".card");
        let currentIndex = 0;
  
        function showCard(index) {
            const cardWidthPercentage = 100 / cards.length;
            cards.forEach((card, i) => {
              card.style.transform = `translateX(${(i - index) * cardWidthPercentage}%)`;
            });
          }          
  
        // Botões de navegação (próximo e anterior)
        document.getElementById("prevPopular").addEventListener("click", () => {
          if (currentIndex > 0) {
            currentIndex--;
            showCard(currentIndex);
          }
        });
  
        document.getElementById("nextPopular").addEventListener("click", () => {
          if (currentIndex < cards.length - 1) {
            currentIndex++;
            showCard(currentIndex);
          }
        });
  
        showCard(currentIndex);
      }
    };
    xmlhttp.send();
  });
  