import os

def upload_to_instance_folder(instance, filename):
    # Obtem a ID do objeto (salvando em uma pasta "unknown" se o objeto não tiver ID ainda)
    obj_id = instance.identifier if instance.identifier else "no-identifier"
    # Cria um caminho dinâmico
    return os.path.join(str(obj_id), filename)
