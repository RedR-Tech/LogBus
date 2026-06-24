// ==========================
// ELEMENTOS
// ==========================
const user = document.getElementById("user_aluno");
const senha = document.getElementById("senha_aluno");
const user_adm = document.getElementById("user_adm");
const senha_adm = document.getElementById("senha_adm");

// =====================
// ABAS
// =====================
const botoes = document.querySelectorAll(".aba-btn");

botoes.forEach((botao) => {

    botao.addEventListener("click", () => {

        document
            .querySelectorAll(".aba-btn")
            .forEach(btn => btn.classList.remove("active"));

        document
            .querySelectorAll(".aba-conteudo")
            .forEach(div => div.classList.remove("active"));

        botao.classList.add("active");

        document
            .getElementById(botao.dataset.tab)
            .classList.add("active");

    });

});

// ==========================
// USUÁRIO ALUNO (10 caracteres)
// ==========================
user.addEventListener("input", () => {

    user.value = user.value.substring(0, 10);

});

// ==========================
// USUÁRIO ADM (10 caracteres)
// ==========================
user_adm.addEventListener("input", () => {

    user_adm.value = user_adm.value.substring(0, 10);

});