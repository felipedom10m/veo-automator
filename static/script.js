/**
 * VEO AUTOMATOR - Script Principal
 * Funcionalidades da interface
 */

let sceneCount = 1;

// ============================================
// INICIALIZAÇÃO
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    loadProfiles();
    setupFormSubmit();

    // Registrar Service Worker para PWA
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/service-worker.js')
            .then(reg => console.log('Service Worker registrado'))
            .catch(err => console.log('Erro ao registrar Service Worker:', err));
    }
});

// ============================================
// CARREGAR PERFIS FLOW
// ============================================

async function loadProfiles() {
    const select = document.getElementById('profile');

    try {
        const response = await fetch('/api/get-profiles');
        const data = await response.json();

        if (data.success) {
            select.innerHTML = '<option value="">Selecione um perfil...</option>';

            data.profiles.forEach(profile => {
                const option = document.createElement('option');
                option.value = profile;
                option.textContent = profile;
                select.appendChild(option);
            });

            if (data.profiles.length === 0) {
                select.innerHTML = '<option value="">Nenhum perfil FLOW encontrado</option>';
                addLog('Nenhum perfil FLOW_ encontrado. Renomeie seus perfis do Chrome.', 'warning');
            }
        } else {
            select.innerHTML = '<option value="">Erro ao carregar perfis</option>';
            addLog('Erro ao carregar perfis: ' + data.error, 'error');
        }
    } catch (error) {
        select.innerHTML = '<option value="">Erro ao conectar com servidor</option>';
        addLog('Erro ao conectar: ' + error.message, 'error');
    }
}

// ============================================
// GERENCIAR CENAS
// ============================================

function addScene() {
    sceneCount++;
    const container = document.getElementById('scenesContainer');

    const sceneItem = document.createElement('div');
    sceneItem.className = 'scene-item';
    sceneItem.innerHTML = `
        <div class="scene-header">
            <span class="scene-number">Cena ${sceneCount}</span>
            <button type="button" class="btn-remove" onclick="removeScene(this)">
                ✕
            </button>
        </div>
        <textarea
            class="scene-textarea"
            placeholder="Cole aqui o prompt da cena..."
            rows="6"
            required
        ></textarea>
    `;

    container.appendChild(sceneItem);
    updateSceneNumbers();
}

function removeScene(button) {
    const sceneItem = button.closest('.scene-item');
    sceneItem.remove();
    updateSceneNumbers();
}

function updateSceneNumbers() {
    const scenes = document.querySelectorAll('.scene-item');
    sceneCount = scenes.length;

    scenes.forEach((scene, index) => {
        const number = index + 1;
        scene.querySelector('.scene-number').textContent = `Cena ${number}`;

        // Mostrar botão de remover apenas se tiver mais de 1 cena
        const removeBtn = scene.querySelector('.btn-remove');
        removeBtn.style.display = scenes.length > 1 ? 'block' : 'none';
    });
}

// ============================================
// SELEÇÃO DE ARQUIVOS/PASTAS
// ============================================

// Variáveis globais para armazenar arquivos selecionados
let selectedImageFile = null;

function handleImageSelect(input) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        selectedImageFile = file;

        // Mostrar nome do arquivo selecionado
        document.getElementById('imagePathDisplay').value = file.name;

        // Mostrar botão de remover
        document.getElementById('removeImageBtn').style.display = 'block';

        addLog('Imagem selecionada: ' + file.name, 'info');
    }
}

function removeImage() {
    selectedImageFile = null;
    document.getElementById('imagePathDisplay').value = '';
    document.getElementById('imageInput').value = '';
    document.getElementById('removeImageBtn').style.display = 'none';
    addLog('Imagem removida', 'info');
}

// ============================================
// SUBMISSÃO DO FORMULÁRIO
// ============================================

function setupFormSubmit() {
    const form = document.getElementById('automationForm');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const btn = document.getElementById('startBtn');
        btn.disabled = true;
        btn.classList.add('loading');

        // Coletar dados do formulário
        const profile = document.getElementById('profile').value;
        const outputFolder = document.getElementById('outputFolderPath').value.trim();

        // Coletar prompts das cenas
        const sceneTextareas = document.querySelectorAll('.scene-textarea');
        const scenes = Array.from(sceneTextareas).map(textarea => textarea.value.trim());

        // Validação
        if (!profile) {
            alert('Selecione um perfil FLOW');
            btn.disabled = false;
            btn.classList.remove('loading');
            return;
        }

        if (scenes.some(scene => !scene)) {
            alert('Preencha todos os prompts das cenas');
            btn.disabled = false;
            btn.classList.remove('loading');
            return;
        }

        if (!outputFolder) {
            alert('Digite o caminho da pasta de destino');
            btn.disabled = false;
            btn.classList.remove('loading');
            return;
        }

        // Mostrar área de logs
        document.getElementById('logsContainer').style.display = 'block';
        clearLogs();

        addLog('Iniciando automação...', 'info');
        addLog(`Perfil: ${profile}`, 'info');
        addLog(`Total de cenas: ${scenes.length}`, 'info');
        if (selectedImageFile) {
            addLog(`Imagem de referência: ${selectedImageFile.name}`, 'info');
        }
        addLog(`Pasta destino: ${outputFolder}`, 'info');

        // Enviar para o backend usando FormData (para suportar upload de arquivo)
        try {
            const formData = new FormData();
            formData.append('profile', profile);
            formData.append('output_folder', outputFolder);
            formData.append('scenes', JSON.stringify(scenes));

            // Adicionar imagem se selecionada
            if (selectedImageFile) {
                formData.append('image', selectedImageFile);
            }

            const response = await fetch('/api/start-automation', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                addLog('✓ ' + data.message, 'success');
                // TODO: Aqui virá a lógica de acompanhamento em tempo real
            } else {
                addLog('✗ Erro: ' + data.error, 'error');
            }

        } catch (error) {
            addLog('✗ Erro ao conectar com servidor: ' + error.message, 'error');
        }

        btn.disabled = false;
        btn.classList.remove('loading');
    });
}

// ============================================
// SISTEMA DE LOGS
// ============================================

function addLog(message, type = 'info') {
    const logsContent = document.getElementById('logsContent');
    const timestamp = new Date().toLocaleTimeString('pt-BR');

    const logItem = document.createElement('div');
    logItem.className = `log-item log-${type}`;
    logItem.textContent = `[${timestamp}] ${message}`;

    logsContent.appendChild(logItem);

    // Auto-scroll para o final
    logsContent.scrollTop = logsContent.scrollHeight;
}

function clearLogs() {
    document.getElementById('logsContent').innerHTML = '';
}

// ============================================
// UTILIDADES
// ============================================

// Prevenir envio acidental do formulário com Enter
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
        if (e.target.form && e.target.type !== 'submit') {
            e.preventDefault();
        }
    }
});
