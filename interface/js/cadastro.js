// Tela de cadastro simples (id + nome), usada por autores.html e generos.html

async function iniciarCadastro(config) {
  const msg = document.getElementById('msg');
  const linhas = document.getElementById('linhas');
  const form = document.getElementById('form-novo');
  const campoNovo = document.getElementById('nome-novo');
  let itens = [];
  let titulos = [];
  let editando = null;

  function livrosDo(item) {
    return titulos.filter(titulo => config.pertence(titulo, item)).map(titulo => titulo.nome);
  }

  function desenhar() {
    if (itens.length === 0) {
      linhas.innerHTML = `<tr><td colspan="4" class="vazio">Nenhum ${config.rotulo} cadastrado.</td></tr>`;
      return;
    }
    linhas.innerHTML = itens.map(item => {
      const livros = livrosDo(item);
      const nome = editando === item.id
        ? `<input class="inp inp-linha" id="nome-editado" value="${escapar(item.nome)}" aria-label="Novo nome">`
        : `<span class="bt">${escapar(item.nome)}</span>`;
      const acoes = editando === item.id
        ? `<button type="button" class="btn btn-p" data-salvar="${item.id}">Salvar</button>
           <button type="button" class="btn" data-cancelar>Cancelar</button>`
        : `<button type="button" class="btn" data-editar="${item.id}">Editar</button>
           <button type="button" class="btn btn-d" data-excluir="${item.id}">Excluir</button>`;
      return `
        <tr>
          <td class="muted">${item.id}</td>
          <td>${nome}</td>
          <td>${livros.length ? escapar(livros.join(', ')) : '<span class="muted">—</span>'}</td>
          <td><div class="actions">${acoes}</div></td>
        </tr>`;
    }).join('');

    const campoEditado = document.getElementById('nome-editado');
    if (campoEditado) campoEditado.focus();
  }

  async function carregar() {
    [itens, titulos] = await Promise.all([api('GET', config.url), api('GET', '/titulo/')]);
    desenhar();
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();
    try {
      await api('POST', config.url, { nome: campoNovo.value.trim() });
      mostrarMensagem(msg, `"${campoNovo.value.trim()}" foi cadastrado.`, 'ok');
      campoNovo.value = '';
      await carregar();
    } catch (erro) {
      mostrarMensagem(msg, erro.message, 'erro');
    }
  });

  linhas.addEventListener('click', async event => {
    const editar = event.target.closest('[data-editar]');
    const salvar = event.target.closest('[data-salvar]');
    const cancelar = event.target.closest('[data-cancelar]');
    const excluir = event.target.closest('[data-excluir]');
    try {
      if (editar) {
        editando = Number(editar.dataset.editar);
        desenhar();
      }
      if (cancelar) {
        editando = null;
        desenhar();
      }
      if (salvar) {
        await api('PUT', `${config.url}${salvar.dataset.salvar}`, { nome: document.getElementById('nome-editado').value.trim() });
        editando = null;
        mostrarMensagem(msg, 'Nome alterado.', 'ok');
        await carregar();
      }
      if (excluir) {
        const item = itens.find(i => i.id === Number(excluir.dataset.excluir));
        if (!confirm(`Excluir "${item.nome}"?`)) return;
        await api('DELETE', `${config.url}${item.id}`);
        mostrarMensagem(msg, `"${item.nome}" foi excluído.`, 'ok');
        await carregar();
      }
    } catch (erro) {
      mostrarMensagem(msg, erro.message, 'erro');
    }
  });

  try {
    await montarCabecalho(config.pagina);
    await carregar();
  } catch (erro) {
    mostrarMensagem(msg, erro.message, 'erro');
  }
}
