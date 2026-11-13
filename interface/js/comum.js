// Funções usadas por todas as telas

async function api(metodo, url, corpo) {
  const opcoes = { method: metodo, headers: {} };
  if (corpo !== undefined) {
    opcoes.headers['Content-Type'] = 'application/json';
    opcoes.body = JSON.stringify(corpo);
  }

  const resposta = await fetch(url, opcoes);
  let dados = null;
  try {
    dados = await resposta.json();
  } catch (erro) {
    dados = null;
  }

  if (resposta.status === 401 && url !== '/usuario/Logar') {
    location.href = 'login.html';
    throw new Error('Faça login primeiro.');
  }
  if (!resposta.ok) {
    throw new Error((dados && dados.erro) || 'Erro ' + resposta.status);
  }
  return dados;
}

function escapar(texto) {
  const div = document.createElement('div');
  div.textContent = texto == null ? '' : String(texto);
  return div.innerHTML;
}

function iniciais(nome) {
  return nome.split(' ').filter(Boolean).slice(0, 2).map(parte => parte[0].toUpperCase()).join('');
}

function parametro(nome) {
  return new URLSearchParams(location.search).get(nome);
}

function mostrarMensagem(elemento, texto, tipo) {
  elemento.textContent = texto;
  elemento.className = 'msg ' + (tipo === 'ok' ? 'msg-ok' : 'msg-erro');
  elemento.hidden = false;
  elemento.scrollIntoView({ block: 'nearest' });
}

function capa(nome, classe) {
  return `<div class="cover ${classe}" role="img" aria-label="Capa de ${escapar(nome)}">${escapar(nome)}</div>`;
}

function formatarData(dataIso) {
  const [ano, mes, dia] = dataIso.split('-');
  return `${dia}/${mes}/${ano}`;
}

// Monta o cabeçalho do design e devolve o usuário logado
async function montarCabecalho(paginaAtiva) {
  const usuario = await api('GET', '/usuario/logado');
  const paginas = [
    ['livros', 'livros.html', 'Livros'],
    ['propostas', 'propostas.html', 'Propostas'],
    ['autores', 'autores.html', 'Autores'],
    ['generos', 'generos.html', 'Gêneros'],
    ['usuarios', 'usuarios.html', 'Usuários'],
  ];

  const menu = paginas.map(([chave, link, texto]) =>
    `<a class="nav${chave === paginaAtiva ? ' nav-on' : ''}" href="${link}">${texto}</a>`).join('');

  document.getElementById('topo').innerHTML = `
    <div class="brand">E-scamboo</div>
    <nav class="menu" aria-label="Principal">${menu}</nav>
    <div class="who">
      <span class="avatar" aria-hidden="true">${escapar(iniciais(usuario.nome))}</span>
      <span>${escapar(usuario.nome)}</span>
      <button type="button" class="btn" id="btn-sair">Sair</button>
    </div>`;

  document.getElementById('btn-sair').addEventListener('click', async () => {
    await api('POST', '/usuario/Deslogar');
    location.href = 'login.html';
  });

  return usuario;
}
