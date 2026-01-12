#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VEO AUTOMATOR - Servidor Flask
Aplicação web PWA para automatizar criação de vídeos no Veo 3
"""

from flask import Flask, render_template, request, jsonify
import os
import json
from automator import detect_flow_profiles

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'veo-automator-2026'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

@app.route('/')
def index():
    """Página principal da aplicação"""
    return render_template('index.html')

@app.route('/api/get-profiles', methods=['GET'])
def get_profiles():
    """
    Retorna lista de perfis FLOW do Chrome
    """
    try:
        # Detectar perfis FLOW automaticamente
        profiles = detect_flow_profiles()

        if not profiles:
            return jsonify({
                'success': True,
                'profiles': [],
                'message': 'Nenhum perfil FLOW encontrado'
            })

        return jsonify({
            'success': True,
            'profiles': profiles
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/start-automation', methods=['POST'])
def start_automation():
    """
    Inicia o processo de automação
    """
    try:
        # Receber dados do FormData
        profile = request.form.get('profile')
        output_folder = request.form.get('output_folder')
        scenes_json = request.form.get('scenes')
        scenes = json.loads(scenes_json) if scenes_json else []

        # Receber arquivo de imagem (se enviado)
        image_file = request.files.get('image')
        image_path = None

        if image_file:
            # Salvar temporariamente a imagem
            import tempfile
            temp_dir = tempfile.gettempdir()
            image_path = os.path.join(temp_dir, image_file.filename)
            image_file.save(image_path)

        # Validações
        if not profile:
            return jsonify({
                'success': False,
                'error': 'Selecione um perfil FLOW'
            }), 400

        if not scenes or len(scenes) == 0:
            return jsonify({
                'success': False,
                'error': 'Adicione pelo menos uma cena'
            }), 400

        if not output_folder:
            return jsonify({
                'success': False,
                'error': 'Selecione a pasta de destino'
            }), 400

        # TODO: Iniciar automação com Selenium
        print(f"[LOG] Perfil selecionado: {profile}")
        print(f"[LOG] Total de cenas: {len(scenes)}")
        print(f"[LOG] Imagem de referência: {image_path if image_path else 'Nenhuma'}")
        print(f"[LOG] Pasta destino: {output_folder}")

        for idx, scene in enumerate(scenes, 1):
            print(f"[LOG] Cena {idx}: {scene[:50]}...")

        return jsonify({
            'success': True,
            'message': 'Automação iniciada com sucesso!'
        })

    except Exception as e:
        print(f"[ERRO] {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🏆 VEO AUTOMATOR - Servidor Iniciado")
    print("=" * 60)
    print("📱 Acesse no navegador:")
    print("   Desktop: http://localhost:5000")
    print("   Mobile:  http://[IP-DA-SUA-MÁQUINA]:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
