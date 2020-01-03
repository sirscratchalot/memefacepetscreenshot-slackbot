import mimetypes
import json

from app import app
from flask import request
from config import Config
from app.inference import LearnerInferer

OK_LOCATION_STARTS=["https://"]
NO_TARGET_ERR={"status":400,"error":"Please provide a url in the ?target query parameter."}
NO_HTTPS={"status":400,"error":"Please provide a url to an HTTPS source."}
NO_MIME_TYPE_ERRO={"status":400,"error":"Please provide a url locating an image."}
inferer=LearnerInferer(Config().MODEL_PATH,Config().MODEL_FILE)
@app.route("/check_image",methods=["GET"])
def check_image():
    target_image=request.args.get("target")
    if(target_image==None):
        return json.dumps(NO_TARGET_ERR),400
    if not target_image.startswith("https://"):
        return json.dumps(NO_HTTPS),400
    mime,encoding = mimetypes.guess_type(target_image)
    if mime==None or not mime.startswith("image"):
        return json.dumps(NO_MIME_TYPE_ERRO),400
    return inferer.infer(image_location=target_image),200
