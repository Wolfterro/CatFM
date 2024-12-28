run:
	@python manage.py runserver

makemigrations:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

shell:
	@python manage.py shell

load_theme:
	@python manage.py loaddata templates/admin_interface_theme_catfm.json

deploy:
	@echo "Instalando dependências..."
	@pip install -r requirements.txt

	@echo "Copiando .env de exemplo..."
	@echo "!!! LEMBRE-SE DE TROCAR O VALOR DO CAMPO DJANGO_SECRET_KEY ANTES DE SUBIR PARA PRODUÇÃO !!!"
	@cp .env.example .env

	@echo "Migrando banco de dados..."
	@python manage.py migrate
	@python manage.py loaddata templates/admin_interface_theme_catfm.json
	@python manage.py loaddata templates/musical_genres.json

	@echo "Deploy concluído! Executando servidor em http://127.0.0.1:8000..."
	@python manage.py runserver

