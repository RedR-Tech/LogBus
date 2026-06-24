// ===================================
// ELEMENTOS GERAIS
// ===================================

const overlay = document.getElementById("overlay");

// ===================================
// ABAS DE ROTA
// ===================================

const botoesAba = document.querySelectorAll(".aba-btn");

botoesAba.forEach(botao => {

    botao.addEventListener("click", () => {

        botoesAba.forEach(btn =>
            btn.classList.remove("active")
        );

        document
            .querySelectorAll(".aba_rota_conteudo")
            .forEach(aba =>
                aba.classList.remove("active")
            );

        botao.classList.add("active");

        const id = botao.dataset.tab;

        document
            .getElementById(id)
            ?.classList.add("active");

    });

});

// ===================================
// MODAIS DE EDIÇÃO
// ===================================

document
    .querySelectorAll(".btn_edit")
    .forEach(botao => {

        botao.addEventListener("click", () => {

            const card =
                botao.closest(".card_aluno");

            const modal =
                card?.querySelector(".box_edit");

            if (!modal) return;

            modal.style.display = "flex";

            overlay?.classList.add("active");

        });

    });

document
    .querySelectorAll(".btn_fechar-edit")
    .forEach(botao => {

        botao.addEventListener("click", () => {

            const modal =
                botao.closest(".box_edit");

            if (!modal) return;

            modal.style.display = "none";

            overlay?.classList.remove("active");

        });

    });

// ===================================
// MODAIS DE EDIÇÃO - ETAPAS
// ===================================

document
    .querySelectorAll(".btn_info-anexo")
    .forEach(botao => {

        botao.addEventListener("click", () => {

            const card =
                botao.closest(".card_aluno");

            card
                ?.querySelector(".box_edit")
                ?.style.setProperty(
                    "display",
                    "none"
                );

            card
                ?.querySelector(".box_edit2")
                ?.style.setProperty(
                    "display",
                    "flex"
                );

        });

    });

document
    .querySelectorAll(".btn_voltar-info1")
    .forEach(botao => {

        botao.addEventListener("click", () => {

            const card =
                botao.closest(".card_aluno");

            card
                ?.querySelector(".box_edit2")
                ?.style.setProperty(
                    "display",
                    "none"
                );

            card
                ?.querySelector(".box_edit")
                ?.style.setProperty(
                    "display",
                    "flex"
                );

        });

    });

// ===================================
// VALIDAÇÕES DOS CAMPOS EDIT
// ===================================

// NOME
document.querySelectorAll(".nome").forEach(campo => {

    campo.addEventListener("input", () => {

        campo.value = campo.value
            .replace(/[^a-zA-ZÀ-ÿ\s]/g, "")
            .substring(0, 50);

    });

});

// USUÁRIO
document.querySelectorAll(".user").forEach(campo => {

    campo.addEventListener("input", () => {

        campo.value = campo.value.substring(0, 10);

    });

});

// FACULDADE
document.querySelectorAll(".faculdade_edit").forEach(campo => {

    campo.addEventListener("input", () => {

        campo.value = campo.value.toUpperCase();

    });

});

// CURSO
document.querySelectorAll(".curso").forEach(campo => {

    campo.addEventListener("input", () => {

        campo.value = campo.value.toUpperCase();

    });

});

// TELEFONE
document.querySelectorAll(".telefone").forEach(campo => {

    campo.addEventListener("input", () => {

        let valor = campo.value.replace(/\D/g, "");

        valor = valor.substring(0, 11);

        valor = valor.replace(
            /^(\d{2})(\d)/,
            "($1) $2"
        );

        valor = valor.replace(
            /(\d{5})(\d)/,
            "$1-$2"
        );

        campo.value = valor;

    });

});

// CPF
document.querySelectorAll(".cpf").forEach(campo => {

    campo.addEventListener("input", () => {

        let valor = campo.value.replace(/\D/g, "");

        valor = valor.substring(0, 11);

        valor = valor.replace(
            /(\d{3})(\d)/,
            "$1.$2"
        );

        valor = valor.replace(
            /(\d{3})(\d)/,
            "$1.$2"
        );

        valor = valor.replace(
            /(\d{3})(\d{1,2})$/,
            "$1-$2"
        );

        campo.value = valor;

    });

});

// ===================================
// MENSAGENS DE ERRO
// ===================================

const mensagemErro = document.querySelector("#registrar_aluno-adm .mensagem_erro");

const mensagemErroAnexo =
    document.getElementById("mensagem_erro-anexo");

// ===================================
// CADASTRO DE ALUNO
// ===================================

const modalCadastro =
    document.getElementById("registrar_aluno-adm");  // era "registrar_aluno"

const modalDocumentos =
    document.getElementById("anexo_documento-adm");  // era "anexo_documento"

const btnProximoCadastro =
    document.getElementById("btn_add-anexo-adm");    // era "btn_add-anexo"

const btnVoltarCadastro =
    document.getElementById("btn_voltar-cadastro");  // igual

const btnFecharCadastro =
    document.getElementById("btn_voltar-adm");       // era "btn_voltar-login"

// ===================================
// ABRIR CADASTRO
// ===================================

document
    .querySelectorAll(".cadastrar_aluno-adm")
    .forEach(botao => {

        botao.addEventListener("click", () => {

            modalCadastro.style.display = "flex";

            modalDocumentos.style.display = "none";

            overlay?.classList.add("active");

        });

    });

// ===================================
// VALIDAÇÃO PRIMEIRA ETAPA
// ===================================

btnProximoCadastro?.addEventListener("click", () => {

    mensagemErro.textContent = "";

    const nome = document.getElementById("nome-adm");
    const usuario = document.getElementById("user-adm");
    const telefone = document.getElementById("telefone-adm");
    const cpf = document.getElementById("cpf-adm");
    const faculdade = document.getElementById("faculdade-adm");
    const curso = document.getElementById("curso-adm");
    const rota = document.getElementById("rota-adm");

    if (
        nome.value.trim() === "" ||
        usuario.value.trim() === "" ||
        telefone.value.trim() === "" ||
        cpf.value.trim() === "" ||
        faculdade.value.trim() === "" ||
        curso.value.trim() === "" ||
        rota.value === ""
    ) {
        mensagemErro.textContent = "Preencha todos os campos.";
        return;
    }

    if (cpf.value.replace(/\D/g, "").length !== 11) {
        mensagemErro.textContent = "CPF inválido.";
        return;
    }

    if (telefone.value.replace(/\D/g, "").length !== 11) {
        mensagemErro.textContent = "Telefone inválido.";
        return;
    }

    modalCadastro.style.display = "none";
    modalDocumentos.style.display = "flex";
});

// ===================================
// VOLTAR ETAPA
// ===================================

btnVoltarCadastro?.addEventListener("click", () => {

    modalDocumentos.style.display = "none";

    modalCadastro.style.display = "flex";

});

// ===================================
// VALIDAÇÃO DE ARQUIVOS
// ===================================

function validarArquivo(arquivo) {
    if (!arquivo) return false;

    const tiposPermitidos = [
        "application/pdf",
        "image/png",
        "image/jpeg"
    ];

    const extensoesPermitidas = [
        ".pdf", ".png", ".jpg", ".jpeg"
    ];

    const extensao = "." + arquivo.name.split(".").pop().toLowerCase();

    const tipoValido = tiposPermitidos.includes(arquivo.type);
    const extensaoValida = extensoesPermitidas.includes(extensao);

    return tipoValido && extensaoValida;
}

// ===================================
// ENVIO DO FORMULÁRIO
// ===================================

const formulario = document.getElementById("form_cadastro"); // <- declarar aqui

formulario?.addEventListener("submit", (e) => {

    mensagemErroAnexo.textContent = "";

    const arquivos = [
        document.getElementById("ft_perfil-adm")?.files[0],
        document.getElementById("rg_frente-adm")?.files[0],
        document.getElementById("rg_verso-adm")?.files[0],
        document.getElementById("comprovante_endereco-adm")?.files[0],
        document.getElementById("comprovante_matricula-adm")?.files[0]
    ];

    const arquivoInvalido = arquivos.some(arquivo => !validarArquivo(arquivo));

    if (arquivoInvalido) {
        mensagemErroAnexo.textContent =
            "Todos os documentos devem estar nos formatos PDF, PNG ou JPG.";
        e.preventDefault();
    }
});

// ===================================
// FECHAR CADASTRO
// ===================================

btnFecharCadastro?.addEventListener(
    "click",
    (e) => {

        e.preventDefault();

        modalCadastro.style.display =
            "none";

        modalDocumentos.style.display =
            "none";

        overlay
            ?.classList
            .remove("active");

    }
);

// ===================================
// CAMPOS COM MÁSCARA (cadastro)
// ===================================

const nome = document.getElementById("nome-adm");
const usuario = document.getElementById("user-adm");
const faculdade = document.getElementById("faculdade-adm");
const curso = document.getElementById("curso-adm");
const telefone = document.getElementById("telefone-adm");
const cpf = document.getElementById("cpf-adm");

// ===================================
// NOME
// ===================================

nome?.addEventListener("input", () => {

    nome.value = nome.value
        .replace(
            /[^a-zA-ZÀ-ÿ\s]/g,
            ""
        )
        .substring(0, 50);

});

// ===================================
// USUÁRIO
// ===================================

usuario?.addEventListener(
    "input",
    () => {

        usuario.value =
            usuario.value.substring(
                0,
                10
            );

    }
);

// ===================================
// FACULDADE
// ===================================

faculdade?.addEventListener(
    "input",
    () => {

        faculdade.value =
            faculdade.value
                .toUpperCase();

    }
);

// ===================================
// CURSO
// ===================================

curso?.addEventListener(
    "input",
    () => {

        curso.value =
            curso.value
                .toUpperCase();

    }
);

// ===================================
// TELEFONE
// ===================================

telefone?.addEventListener(
    "input",
    () => {

        let valor =
            telefone.value.replace(
                /\D/g,
                ""
            );

        valor =
            valor.substring(
                0,
                11
            );

        valor =
            valor.replace(
                /^(\d{2})(\d)/,
                "($1) $2"
            );

        valor =
            valor.replace(
                /(\d{5})(\d)/,
                "$1-$2"
            );

        telefone.value =
            valor;

    }
);

// ===================================
// CPF
// ===================================

cpf?.addEventListener(
    "input",
    () => {

        let valor =
            cpf.value.replace(
                /\D/g,
                ""
            );

        valor =
            valor.substring(
                0,
                11
            );

        valor =
            valor.replace(
                /(\d{3})(\d)/,
                "$1.$2"
            );

        valor =
            valor.replace(
                /(\d{3})(\d)/,
                "$1.$2"
            );

        valor =
            valor.replace(
                /(\d{3})(\d{1,2})$/,
                "$1-$2"
            );

        cpf.value =
            valor;

    }
);

// Pesquisa Goiânia
document.getElementById('pesquisa_aluno-goiania').addEventListener('input', function () {
    filtrarAlunos(this.value, 'rota_goiania');
});

// Pesquisa Trindade
document.getElementById('pesquisa_aluno-trindade').addEventListener('input', function () {
    filtrarAlunos(this.value, 'rota_trindade');
});

function filtrarAlunos(termo, rotaId) {
    const cards = document.querySelectorAll(`#${rotaId} .card_aluno`);
    const termoBusca = termo.toLowerCase().trim();

    cards.forEach(card => {
        const nome = card.querySelector('.dados_aluno h3')?.textContent.toLowerCase() || '';
        const telefone = card.querySelector('.dados_aluno p')?.textContent.toLowerCase() || '';

        const visivel = nome.includes(termoBusca) || telefone.includes(termoBusca);
        card.style.display = visivel ? '' : 'none';
    });
}