import base64
import pandas as pd
from sklearn.feature_extraction import FeatureHasher


class Audio2Vec:
    def __init__(self, nFeatures=11, inputType='string'):
        self.hasher = FeatureHasher(n_features=nFeatures, input_type=inputType)

    @staticmethod
    def b64Wav2string(wavPath):
        """Convert audio to base64 string."""
        with open(wavPath, "rb") as wavFile:
            wavData = wavFile.read()
        return base64.b64encode(wavData).decode("utf-8")

    def hashedString2Vec(self, hashedString):
        """Convert hashed string to vector."""
        return self.hasher.transform([list(hashedString)])

    def audio2VectorProcessor(self, wavPath):
        """convert hashed string to vector"""
        hashedString = self.b64Wav2string(wavPath)
        vectorisedHashedString = self.hashedString2Vec(hashedString)
        return vectorisedHashedString

    @staticmethod
    def convertVec2List(vectorisedFeatures):
        """Convert vectorised features to list."""
        return vectorisedFeatures.toarray().tolist()[0]

    def audio2ListProcessor(self, wavPath):
        """convert audio to list of elements"""
        vectorisedHashedString = self.audio2VectorProcessor(wavPath)
        convertVectorisedHashedString2List = self.convertVec2List(vectorisedHashedString)
        return convertVectorisedHashedString2List

    @staticmethod
    def convertList2Df(vectorisedList):
        """Convert list to DataFrame."""
        columns = [f"features-{i + 1}" for i in range(len(vectorisedList))]
        return pd.DataFrame([vectorisedList], columns=columns)

    def audio2Vec2DfProcessor(self, wavPath):
        """Process the wav file and return a DataFrame of features."""
        hashedString = self.b64Wav2string(wavPath)
        vectorisedFeatures = self.hashedString2Vec(hashedString)
        vectorisedList = self.convertVec2List(vectorisedFeatures)
        return self.convertList2Df(vectorisedList)

