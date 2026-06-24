// ==========================
// HORÁRIOS DO ÔNIBUS
// ==========================
const horarios = [
    { h: 6,  m: 0,  tipo: 'ida',   desc: 'Manhã · Ida',   id: 'h_manha_ida'   },
    { h: 11, m: 30, tipo: 'volta',  desc: 'Manhã · Volta', id: 'h_manha_volta' },
    { h: 12, m: 20, tipo: 'ida',    desc: 'Tarde · Ida',   id: 'h_tarde_ida'   },
    { h: 17, m: 35, tipo: 'volta',  desc: 'Tarde · Volta', id: 'h_tarde_volta' },
];

// ==========================
// FUNÇÕES AUXILIARES
// ==========================
function toMinutos(h, m) {
    return h * 60 + m;
}

function formatarHora(h, m) {
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
}

// ==========================
// ATUALIZAR HORÁRIOS
// ==========================
function atualizarHorarios() {

    const agora = new Date();
    const agoraMin = toMinutos(agora.getHours(), agora.getMinutes());

    let proximoIdx = -1;

    horarios.forEach((horario, i) => {

        const el = document.getElementById(horario.id);

        if (!el) return;

        const horarioMin = toMinutos(horario.h, horario.m);

        // Remove classes anteriores
        el.classList.remove('passado', 'proximo', 'futuro');

        // Remove badge anterior se existir
        const badgeAntigo = el.querySelector('.tag_proximo_badge');
        if (badgeAntigo) badgeAntigo.remove();

        if (horarioMin < agoraMin) {
            el.classList.add('passado');

        } else if (proximoIdx === -1) {
            proximoIdx = i;
            el.classList.add('proximo');

            const badge = document.createElement('span');
            badge.className = 'tag_proximo_badge';
            badge.textContent = '● Próximo';
            el.appendChild(badge);

        } else {
            el.classList.add('futuro');
        }

    });

    // ==========================
    // ATUALIZAR DESTAQUE
    // ==========================
    const proximoHorario = document.getElementById('proximo_horario');
    const proximoDesc    = document.getElementById('proximo_tipo_desc');
    const tempoNumero    = document.getElementById('tempo_numero');
    const tempoLabel     = document.getElementById('tempo_label');
    const proximoIcone   = document.getElementById('proximo_icone').querySelector('i');

    if (proximoIdx !== -1) {

        const pr   = horarios[proximoIdx];
        const diff = toMinutos(pr.h, pr.m) - agoraMin;

        proximoHorario.textContent = formatarHora(pr.h, pr.m);
        proximoDesc.textContent    = pr.desc;
        tempoNumero.textContent    = diff;
        tempoLabel.textContent     = 'min';

        // Ícone muda conforme ida ou volta
        if (pr.tipo === 'ida') {
            proximoIcone.className = 'fa-solid fa-arrow-right';
        } else {
            proximoIcone.className = 'fa-solid fa-rotate-left';
        }

    } else {

        proximoHorario.textContent = '--:--';
        proximoDesc.textContent    = 'Sem mais horários hoje';
        tempoNumero.textContent    = '--';
        tempoLabel.textContent     = '';
        proximoIcone.className     = 'fa-solid fa-bus';

    }

}

// ==========================
// INICIAR
// ==========================
atualizarHorarios();

setInterval(atualizarHorarios, 30000);
