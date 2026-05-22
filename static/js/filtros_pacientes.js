document.addEventListener("DOMContentLoaded", function () {
  var campoScoreMinimo = document.getElementById("filtro_score_minimo");
  var campoScoreMaximo = document.getElementById("filtro_score_maximo");
  var campoSexo = document.getElementById("filtro_sexo");
  var campoUsuario = document.getElementById("filtro_usuario");
  var botaoLimpar = document.getElementById("limpar_filtros");
  var contadorResultados = document.getElementById("contador_resultados");
  var linhasAvaliacoes = document.querySelectorAll(".linha-avaliacao");
  var linhaSemResultados = document.getElementById("linha_sem_resultados");

  function converterScoreParaNumero(textoScore) {
    if (textoScore === "") {
      return null;
    }

    return Number(textoScore);
  }

  function linhaPassaNoScore(linha, scoreMinimo, scoreMaximo) {
    var scoreLinha = converterScoreParaNumero(linha.getAttribute("data-score"));

    if (scoreMinimo !== null && scoreLinha < scoreMinimo) {
      return false;
    }

    if (scoreMaximo !== null && scoreLinha > scoreMaximo) {
      return false;
    }

    return true;
  }

  function linhaPassaNoSexo(linha, sexoSelecionado) {
    if (sexoSelecionado === "") {
      return true;
    }

    return linha.getAttribute("data-sexo") === sexoSelecionado;
  }

  function linhaPassaNoUsuario(linha, usuarioSelecionado) {
    if (usuarioSelecionado === "") {
      return true;
    }

    return linha.getAttribute("data-usuario") === usuarioSelecionado;
  }

  function atualizarTabela() {
    var scoreMinimo = converterScoreParaNumero(campoScoreMinimo.value);
    var scoreMaximo = converterScoreParaNumero(campoScoreMaximo.value);
    var sexoSelecionado = campoSexo.value;
    var usuarioSelecionado = campoUsuario.value;
    var totalVisivel = 0;

    for (var indice = 0; indice < linhasAvaliacoes.length; indice++) {
      var linha = linhasAvaliacoes[indice];
      var passouNoScore = linhaPassaNoScore(linha, scoreMinimo, scoreMaximo);
      var passouNoSexo = linhaPassaNoSexo(linha, sexoSelecionado);
      var passouNoUsuario = linhaPassaNoUsuario(linha, usuarioSelecionado);

      if (passouNoScore && passouNoSexo && passouNoUsuario) {
        linha.hidden = false;
        totalVisivel = totalVisivel + 1;
      } else {
        linha.hidden = true;
      }
    }

    contadorResultados.textContent = "Resultados visíveis: " + totalVisivel;

    if (linhaSemResultados) {
      linhaSemResultados.hidden = totalVisivel !== 0;
    }
  }

  function limparFiltros() {
    campoScoreMinimo.value = "";
    campoScoreMaximo.value = "";
    campoSexo.value = "";
    campoUsuario.value = "";
    atualizarTabela();
  }

  campoScoreMinimo.addEventListener("input", atualizarTabela);
  campoScoreMaximo.addEventListener("input", atualizarTabela);
  campoSexo.addEventListener("change", atualizarTabela);
  campoUsuario.addEventListener("change", atualizarTabela);
  botaoLimpar.addEventListener("click", limparFiltros);

  atualizarTabela();
});
