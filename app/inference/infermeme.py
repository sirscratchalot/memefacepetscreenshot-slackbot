from fastai.vision import open_image
from fastai.vision import load_learner
from os.path import abspath as Path
from requests import get
from io import BytesIO
from collections import OrderedDict
import json
import os


class LearnerInferer:
    learner = None

    def __init__(self, path, model):
        print(path, model)
        self.learner = load_learner(path, model)

    def infer(self, image_location: str, headers: dict = None):
        if image_location.startswith("http"):
            image_response = get(url=image_location, headers=headers)
            print("Attempted to retrieve image: ", image_response.status_code)
            if(image_response.status_code == 200):
                image = open_image(BytesIO(image_response.content))
                return self._buildResponse(image)
            else:
                return "Could not retrieve image!"
        else:
            image = open_image(image_location)
            return self._buildResponse(image)

    def _buildResponse(self, image):
        pred_class, _, losses = self.learner.predict(image)
        json_dict = OrderedDict({"predicted_class": str(pred_class)})
        probabilities = {self.learner.data.classes[i]:
                         round(100.*prob.item(), 2)
                         for i, prob in enumerate(losses)}

        for item in sorted(probabilities.items(), key=lambda i: -i[1]):
            json_dict[item[0]] = item[1]

        return json_dict


# Replace with test
if __name__ == "__main__":
    REMOTE_URL = os.environ.get("MEME_URL") or "https://2.bp.blogspot.com/-yP5-Dr53gJ0/Un9EayUUYLI/AAAAAAAAAzI/j0ryJiYSAk4/s1600/ferfe.jpg"
    LOCAL_IMAGE = os.environ.get("LOCAL_IMAGE") or "/home/erik/Pictures/Skärmbild från 2013-12-07 19:24:53.png"
    path, model = Path("../../models"), "memepetfacescreen.pkl"
    inferer = LearnerInferer(path, model)
    print(json.dumps(inferer.infer(REMOTE_URL)))
    print(json.dumps(inferer.infer(LOCAL_IMAGE)))
