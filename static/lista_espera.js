const botoes = document.querySelectorAll(".aba-btn");

botoes.forEach(botao => {

    botao.addEventListener("click", () => {

        // Remove botão ativo
        document.querySelectorAll(".aba-btn")
            .forEach(btn => btn.classList.remove("active"));

        // Esconde todas as abas
        document.querySelectorAll(".aba_rota_conteudo")
            .forEach(aba => aba.classList.remove("active"));

        // Ativa botão clicado
        botao.classList.add("active");

        // Mostra a aba correspondente
        const id = botao.dataset.tab;

        document.getElementById(id)
            .classList.add("active");
    });

});

const overlay = document.getElementById("overlay");

const btnsInfo =
    document.querySelectorAll(".btn_info");

const btnsFechar =
    document.querySelectorAll(".btn_fechar-info");

btnsInfo.forEach((botao) => {

    botao.addEventListener("click", () => {

        const card =
            botao.closest(".card_aluno");

        const boxInfo =
            card.querySelector(".box_info");

        boxInfo.style.display = "flex";

        overlay.classList.add("active");

    });

});

btnsFechar.forEach((botao) => {

    botao.addEventListener("click", () => {

        const boxInfo =
            botao.closest(".box_info");

        boxInfo.style.display = "none";

        overlay.classList.remove("active");

    });

});

// ==========================
// BOTÃO PRÓXIMO
// ==========================
const btnsProximo =
    document.querySelectorAll(".btn_info-anexo");

btnsProximo.forEach((botao) => {

    botao.addEventListener("click", () => {

        const card =
            botao.closest(".card_aluno");

        const boxInfo =
            card.querySelector(".box_info");

        const boxInfo2 =
            card.querySelector(".box_info2");

        boxInfo.style.display = "none";
        boxInfo2.style.display = "flex";

    });

});

// ==========================
// BOTÃO VOLTAR
// ==========================
const btnsVoltar =
    document.querySelectorAll(".btn_voltar-info1");

btnsVoltar.forEach((botao) => {

    botao.addEventListener("click", () => {

        const card =
            botao.closest(".card_aluno");

        const boxInfo =
            card.querySelector(".box_info");

        const boxInfo2 =
            card.querySelector(".box_info2");

        boxInfo2.style.display = "none";
        boxInfo.style.display = "flex";

    });

});