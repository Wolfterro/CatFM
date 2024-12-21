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
