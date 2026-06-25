// ==========================
// ELEMENTOS
// ==========================
const formulario = document.getElementById("form_cadastro");

const nome = document.getElementById("nome");
const user = document.getElementById("user");
const telefone = document.getElementById("telefone");
const cpf = document.getElementById("cpf");
const email = document.getElementById("email");
const senha = document.getElementById("register_senha_aluno");
const faculdade = document.getElementById("faculdade");
const curso = document.getElementById("curso");
const rota = document.getElementById("rota");

const btnProximo = document.getElementById("btn_add-anexo");
const btnVoltarCadastro = document.getElementById("btn_voltar-cadastro");

const cadastroAluno = document.getElementById("registrar_aluno");
const anexoDocumento = document.getElementById("anexo_documento");

const mensagemErro = document.getElementById("mensagem_erro");
const mensagemErroAnexo = document.getElementById("mensagem_erro-anexo")

const MODO_TESTE = false;

// ==========================
// NOME (50 caracteres)
// ==========================
nome.addEventListener("input", () => {

    nome.value = nome.value
        .replace(/[^a-zA-ZÀ-ÿ\s]/g, "")
        .substring(0, 50);

});

// ==========================
// USUÁRIO (10 caracteres)
// ==========================
user.addEventListener("input", () => {

    user.value = user.value.substring(0, 10);

});

// ==========================
// FACULDADE MAIÚSCULO
// ==========================
faculdade.addEventListener("input", () => {

    faculdade.value = faculdade.value.toUpperCase();

});

// ==========================
// CURSO MAIÚSCULO
// ==========================
curso.addEventListener("input", () => {

    curso.value = curso.value.toUpperCase();

});

// ==========================
// MÁSCARA TELEFONE
// ==========================
telefone.addEventListener("input", () => {

    let valor = telefone.value.replace(/\D/g, "");

    valor = valor.substring(0, 11);

    valor = valor.replace(/^(\d{2})(\d)/, "($1) $2");
    valor = valor.replace(/(\d{5})(\d)/, "$1-$2");

    telefone.value = valor;

});

// ==========================
// MÁSCARA CPF
// ==========================
cpf.addEventListener("input", () => {

    let valor = cpf.value.replace(/\D/g, "");

    valor = valor.substring(0, 11);

    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    cpf.value = valor;

});

// ==========================
// VERIFICAR DUPLICADOS
// ==========================

async function verificarCampo(url, spanId) {
    const span = document.getElementById(spanId);
    try {
        const res = await fetch(url);
        const data = await res.json();
        if (data.existe) {
            span.textContent = "Já cadastrado no sistema!";
            return true;
        } else {
            span.textContent = "";
            return false;
        }
    } catch {
        span.textContent = "";
        return false;
    }
}

cpf.addEventListener("blur", () => {
    if (validarCPF(cpf.value)) {
        verificarCampo(`/verificar/cpf/${cpf.value}`, "erro_cpf");
    }
});

email.addEventListener("blur", () => {
    if (email.value.trim() !== "") {
        verificarCampo(`/verificar/email/${email.value}`, "erro_email");
    }
});

user.addEventListener("blur", () => {
    if (user.value.trim() !== "") {
        verificarCampo(`/verificar/usuario/${user.value}`, "erro_user");
    }
});

// ==========================
// VALIDAR CPF
// ==========================
function validarCPF(cpf) {

    cpf = cpf.replace(/\D/g, "");

    if (cpf.length !== 11) return false;

    if (/^(\d)\1+$/.test(cpf)) return false;

    // Ignora o cálculo dos dígitos verificadores
    if (MODO_TESTE) {
        return true;
    }

    let soma = 0;

    for (let i = 0; i < 9; i++) {
        soma += Number(cpf[i]) * (10 - i);
    }

    let resto = (soma * 10) % 11;

    if (resto === 10) resto = 0;

    if (resto !== Number(cpf[9])) return false;

    soma = 0;

    for (let i = 0; i < 10; i++) {
        soma += Number(cpf[i]) * (11 - i);
    }

    resto = (soma * 10) % 11;

    if (resto === 10) resto = 0;

    if (resto !== Number(cpf[10])) return false;

    return true;
}

// ==========================
// VALIDAR SENHA
// ==========================
function validarSenha(senha) {

    if (MODO_TESTE) {
        return true;
    }
    const regex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#])[A-Za-z\d@$!%*?&.#]{8,}$/;

    return regex.test(senha);
}

// ==========================
// BOTÃO PRÓXIMO
// ==========================
btnProximo.addEventListener("click", () => {
    const cpfDuplicado = document.getElementById("erro_cpf").textContent !== "";
    const emailDuplicado = document.getElementById("erro_email").textContent !== "";
    const userDuplicado = document.getElementById("erro_user").textContent !== "";

    if (cpfDuplicado || emailDuplicado || userDuplicado) {
        mensagemErro.textContent = "Corrija os campos em vermelho antes de continuar.";
        return;
    }

    mensagemErro.textContent = "";

    if (
        nome.value.trim() === "" ||
        user.value.trim() === "" ||
        telefone.value.trim() === "" ||
        cpf.value.trim() === "" ||
        email.value.trim() === "" ||
        senha.value.trim() === "" ||
        faculdade.value.trim() === "" ||
        curso.value.trim() === "" ||
        rota.value === ""
    ) {

        mensagemErro.textContent =
            "Preencha todos os campos.";

        return;
    }

    if (!validarCPF(cpf.value)) {

        mensagemErro.textContent =
            "CPF inválido.";

        return;
    }

    if (telefone.value.replace(/\D/g, "").length !== 11) {

        mensagemErro.textContent =
            "Telefone inválido.";

        return;
    }

    if (!validarSenha(senha.value)) {

        mensagemErro.textContent =
            "Senha deve conter 8 caracteres, letra maiúscula, minúscula, número e símbolo.";

        return;
    }

    cadastroAluno.style.display = "none";
    anexoDocumento.style.display = "block";

});

// ==========================
// VOLTAR
// ==========================
btnVoltarCadastro.addEventListener("click", () => {

    anexoDocumento.style.display = "none";
    cadastroAluno.style.display = "flex";

});

// ==========================
// VALIDAR DOCUMENTOS
// ==========================
function validarArquivo(arquivo) {

    if (!arquivo) return false;

    const extensoesPermitidas = [
        "application/pdf",
        "image/png",
        "image/jpeg"
    ];

    return extensoesPermitidas.includes(arquivo.type);
}

// ==========================
// SUBMIT FINAL
// ==========================
formulario.addEventListener("submit", (e) => {

    mensagemErroAnexo.textContent = "";

    const rgFrente =
        document.getElementById("rg_frente").files[0];

    const rgVerso =
        document.getElementById("rg_verso").files[0];

    const endereco =
        document.getElementById("comprovante_endereco").files[0];

    const matricula =
        document.getElementById("comprovante_matricula").files[0];

    if (
        !validarArquivo(rgFrente) ||
        !validarArquivo(rgVerso) ||
        !validarArquivo(endereco) ||
        !validarArquivo(matricula)
    ) {

        mensagemErroAnexo.textContent =
            "Todos os documentos devem estar nos formatos PDF, PNG ou JPG.";

        e.preventDefault();
        return;
    }

});