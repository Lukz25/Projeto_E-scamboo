// Formulário usado em novo-livro.html e editar-livro.html

function criarSeletor(caixa, select, opcoes, rotulo) {
  const selecionados = [];

  function desenhar() {
    caixa.classList.toggle('multi-on', selecionados.length > 0);
    caixa.innerHTML = selecionados.length === 0
      ? '<span class="vazio-multi">Selecione um ou mais</span>'
      : selecionados.map(id => {
          const opcao = opcoes.find(o => o.id === id);
          return `<span class="chip">${escapar(opcao.nome)} <button type="button" data-remover="${id}" aria-label="Remover ${escapar(opcao.nome)}">×</button></span>`;
        }).join('');

    const disponiveis = opcoes.filter(o => !selecionados.includes(o.id));
    select.innerHTML = `<option value="">+ Adicionar ${rotulo}</option>` +
      disponiveis.map(o => `<option value="${o.id}">${escapar(o.nome)}</option>`).join('');
  }

  caixa.addEventListener('click', event => {
    const botao = event.target.closest('[data-remover]');
    if (botao) {
      selecionados.splice(selecionados.indexOf(Number(botao.dataset.remover)), 1);
      desenhar();
    }
  });
  select.addEventListener('change', () => {
    if (select.value) {
      selecionados.push(Number(select.value));
      desenhar();
    }
  });

  desenhar();
  return {
    definir(ids) {
      selecionados.splice(0, selecionados.length, ...ids);
      desenhar();
    },
    valores() {
      return [...selecionados];
    },
  };
}

async function iniciarFormularioLivro(idTitulo) {
  const msg = document.getElementById('msg');
  const form = document.getElementById('form-livro');
  const campoNome = document.getElementById('nome');
  const campoData = document.getElementById('data');
  const campoEstado = document.getElementById('estado');
  const campoDescricao = document.getElementById('descricao');

  try {
    const eu = await montarCabecalho('livros');
    const nomeDono = document.getElementById('nome-dono');
    if (nomeDono) nomeDono.textContent = eu.nome;

    const [autores, generos] = await Promise.all([api('GET', '/autor/'), api('GET', '/genero/')]);
    const seletorAutores = criarSeletor(document.getElementById('caixa-autores'), document.getElementById('add-autor'), autores, 'autor');
    const seletorGeneros = criarSeletor(document.getElementById('caixa-generos'), document.getElementById('add-genero'), generos, 'gênero');

    if (idTitulo) {
      const titulo = await api('GET', `/titulo/${idTitulo}`);
      if (titulo.dono !== eu.email) {
        mostrarMensagem(msg, 'Só o dono pode editar este livro.', 'erro');
        form.querySelectorAll('input, select, textarea, button').forEach(campo => campo.disabled = true);
      }
      campoNome.value = titulo.nome;
      campoData.value = titulo.data_lancamento;
      campoEstado.value = titulo.estado_conservacao;
      campoDescricao.value = titulo.descricao;
      seletorAutores.definir(titulo.autores_ids);
      seletorGeneros.definir(titulo.generos_ids);
      document.getElementById('capa-titulo').textContent = titulo.nome;
      campoNome.addEventListener('input', () => {
        document.getElementById('capa-titulo').textContent = campoNome.value || titulo.nome;
      });

      document.getElementById('btn-excluir').addEventListener('click', async () => {
        if (!confirm(`Excluir "${titulo.nome}"?`)) return;
        try {
          await api('DELETE', `/titulo/${idTitulo}`);
          location.href = 'livros.html';
        } catch (erro) {
          mostrarMensagem(msg, erro.message, 'erro');
        }
      });
    }

    form.addEventListener('submit', async event => {
      event.preventDefault();
      const dados = {
        nome: campoNome.value.trim(),
        autores: seletorAutores.valores(),
        generos: seletorGeneros.valores(),
        data_lancamento: campoData.value.trim(),
        estado_conservacao: campoEstado.value,
        descricao: campoDescricao.value.trim(),
      };
      if (!dados.nome) {
        mostrarMensagem(msg, 'Informe o título do livro.', 'erro');
        return;
      }
      try {
        if (idTitulo) {
          await api('PUT', `/titulo/${idTitulo}`, dados);
        } else {
          await api('POST', '/titulo/', dados);
        }
        location.href = 'livros.html';
      } catch (erro) {
        mostrarMensagem(msg, erro.message, 'erro');
      }
    });
  } catch (erro) {
    mostrarMensagem(msg, erro.message, 'erro');
  }
}
