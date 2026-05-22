document.addEventListener("DOMContentLoaded", function () {
  var campoSexo = document.getElementById("sexo_paciente");
  var sintomasMasculinos = document.querySelectorAll("[data-apenas-masculino='sim']");

  function atualizarMacroorquidismo() {
    var sexoSelecionado = campoSexo.value;

    for (var indice = 0; indice < sintomasMasculinos.length; indice++) {
      var linhaSintoma = sintomasMasculinos[indice];
      var caixaMarcacao = linhaSintoma.querySelector("input[type='checkbox']");

      if (sexoSelecionado === "F") {
        caixaMarcacao.checked = false;
        caixaMarcacao.disabled = true;
        linhaSintoma.hidden = true;
      } else {
        caixaMarcacao.disabled = false;
        linhaSintoma.hidden = false;
      }
    }
  }

  if (campoSexo) {
    campoSexo.addEventListener("change", atualizarMacroorquidismo);
    atualizarMacroorquidismo();
  }
});
