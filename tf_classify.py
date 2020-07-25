import time
from lobe import ImageModel
from lobe.Signature import Signature
import lobe

start_time = time.time()
#model:ImageModel = ImageModel.load('~/code/bee/BeeCam/tf_models')
#sig: Signature = Signature('/home/pi/code/bee/BeeCam/tf_models_lite')
#model: ImageModel = ImageModel.load_from_signature(sig)
model: ImageModel = ImageModel.load('/home/pi/code/bee/BeeCam/tf_models_lite')

'''
The TFClassify class (Tensor Flow Classifier), takes a TensorFlow model and allows you
to pass multiple images to it via the addImage() or addImages() methods. It then
returns the predicted classification of the images as a DICT array
{
    'image': '<image_path_sent_to_classifier>',
    'prediction': 'output_prediction_from_TensorFlow'>
}
'''
class TFClassify:
    def __init__(self):
        self.images = []
        self.results = []
    

    #Add a single image to the classifier
    def addImage(self, imagePath) -> int:
        self.images.append(imagePath)
        return len(self.images)
    

    #Add an array of images to the classifier
    def addImages(self, imagePaths:[]) -> int:
        self.images = imagePaths
        return len(self.images)


    #Clears the image array
    def reset(self):
        self.images, self.results = [], []
    

    '''For each image in the images collection, process it, and then return
        an array of results. Each item in the array is a dictionary:
        {image:<image_path>, prediction:<prediction_from_tensorflow>}
    '''
    def doClassify(self) -> []:
        for item in self.images:
            res = model.predict_from_file(item)
            predict = res.prediction
            result = {"image": item, "prediction": predict, "confidence":"X"}
            self.results.append(result)
        
        #self.results = [model.predict_from_file(item).prediction for item in self.images]
        return self.results
            

if __name__ == '__main__':
    classifier = TFClassify()
    #print(f"TensorFlow load took {time.time() - start_time} seconds")
    start_time = time.time()
    classifier.reset()
    classifier.addImage('/home/pi/code/bee/BeeCam/tf_models/1.jpeg')
    classifier.addImage('/home/pi/code/bee/BeeCam/tf_models/2.jpeg')
    results = classifier.doClassify()
    #print(f"TensorFlow classification took {time.time() - start_time} seconds")
    for r in results:
        print(r)
