import base64
import PIL.Image as Image
from io import BytesIO

from pymongo import MongoClient
from flask import Flask, request, jsonify

#DIRETORIO = "/home/gustavo/PycharmProjects/upandoimage/flask-salvar-arquivos/output"

api = Flask(__name__)
client = MongoClient("mongodb://localhost/27017")
db = client.imgs

'''salve file'''
def save_manager(datab, target):
    id = 0
    for img in datab.images.find({}):
        id += 1

    datab.images.insert_one({
        "_id": id,
        "file": base64.b64encode(target.stream.read())
    })

    result = {
        "msg":"Ok"
    }

    return jsonify(result)


'''
    mostra imagem dentro do database pelo id autoincrementado
'''
@api.route("/img/<int:id>")
def show_img(id):
    image = db.images.find_one({"_id": id})
    if image:
        img = Image.open(BytesIO(base64.b64decode(image["file"])))
        img.show()
        return jsonify({"msg":"show image"})
    else:
        return jsonify({"msg":"image not found"})

'''
SALVAR ARQUIVO NO DB
'''
@api.route("/arquivos", methods=["POST"])
def post_arquivo():
    file = request.files.get("meuArquivo")

    file_name = file.filename
    #arquivo.save(os.path.join(DIRETORIO, nome_do_arquivo))

    #file_path = os.path.join(DIRETORIO, file_name)

    return save_manager(db, file)


if __name__ == "__main__":
    api.run(debug=True, port=8000)


# @api.route("/arquivos", methods=["GET"])
# def lista_arquivos():
#     arquivos = []
#
#     for nome_do_arquivo in os.listdir(DIRETORIO):
#         endereco_do_arquivo = os.path.join(DIRETORIO, nome_do_arquivo)
#
#         if(os.path.isfile(endereco_do_arquivo)):
#             arquivos.append(nome_do_arquivo)
#
#     return jsonify(arquivos)
# '''
# retornar arquivo
# '''
# @api.route("/arquivos/<nome_do_arquivo>",  methods=["GET"])
# def get_arquivo(nome_do_arquivo):
#     return send_from_directory(DIRETORIO, nome_do_arquivo, as_attachment=True)