// Máscaras de CPF/telefone e exibição do erro do servidor.
// Toda validação de regra de negócio fica no backend (schemas.py).

document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("triagem-form");
    if (!form) return;

    var cpf               = document.getElementById("cpf");
    var telefone          = document.getElementById("telefone");
    var telefoneResp      = document.getElementById("telefone_responsavel");

    function somenteDigitos(valor) {
        return (valor || "").replace(/\D/g, "");
    }

    function bloquearLetras(e) {
        if (e.data && /\D/.test(e.data)) e.preventDefault();
    }

    function mascaraCpf(valor) {
        var n = somenteDigitos(valor).slice(0, 11);
        return n
            .replace(/^(\d{3})(\d)/, "$1.$2")
            .replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3")
            .replace(/\.(\d{3})(\d)/, ".$1-$2");
    }

    function mascaraTelefone(valor) {
        var n = somenteDigitos(valor).slice(0, 11);
        if (n.length <= 10) {
            return n.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{4})(\d)/, "$1-$2");
        }
        return n.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{5})(\d)/, "$1-$2");
    }

    function aplicarMascara(campo, mascara) {
        if (!campo) return;
        campo.addEventListener("beforeinput", bloquearLetras);
        campo.addEventListener("input", function () {
            campo.value = mascara(campo.value);
        });
        campo.value = mascara(campo.value);
    }

    aplicarMascara(cpf, mascaraCpf);
    aplicarMascara(telefone, mascaraTelefone);
    aplicarMascara(telefoneResp, mascaraTelefone);

    // Exibe o erro do servidor no campo correspondente via tooltip nativo.
    if (form.dataset.serverError) {
        var campoErro = form.dataset.serverField
            ? form.elements[form.dataset.serverField]
            : null;
        var alvo = (campoErro && campoErro.setCustomValidity)
            ? campoErro
            : form.querySelector("input:not([type='hidden']), select, textarea");

        alvo.setCustomValidity(form.dataset.serverError);
        alvo.reportValidity();
        alvo.addEventListener("input", function () {
            alvo.setCustomValidity("");
        }, { once: true });
    }
});
