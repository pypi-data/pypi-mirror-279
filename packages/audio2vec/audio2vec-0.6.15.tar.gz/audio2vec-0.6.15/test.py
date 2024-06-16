import base64
import pandas as pd
from sklearn.feature_extraction import FeatureHasher

hasher = FeatureHasher(n_features=5, input_type="string")


def b64Wav2string(wavPath):
    """Convert audio to base64 string."""
    with open(wavPath, "rb") as wavFile:
        wavData = wavFile.read()
    return base64.b64encode(wavData).decode("utf-8")


def hashedString2Vec(hashedString):
    """Convert hashed string to vector."""
    hashedStrings = hasher.transform([list(hashedString)])
    return hashedStrings


def audio2VectorProcessor(wavPath):
    """convert hashed string to vector"""
    hashedString = b64Wav2string(wavPath)
    vectorisedHashedString = hashedString2Vec(hashedString)
    return vectorisedHashedString


def convertVec2List(vectorisedFeatures):
    """Convert vectorised features to list."""
    return vectorisedFeatures.toarray().tolist()[0]


def audio2ListProcessor(wavPath):
    """convert audio to list of elements"""
    vectorisedHashedString = audio2VectorProcessor(wavPath)
    convertVectorisedHashedString2List = convertVec2List(vectorisedHashedString)
    return convertVectorisedHashedString2List


def convertList2Df(vectorisedList):
    """Convert list to DataFrame."""
    columns = [f"features-{i + 1}" for i in range(len(vectorisedList))]
    return pd.DataFrame([vectorisedList], columns=columns)


def audio2Vec2DfProcessor(wavPath):
    """Process the wav file and return a DataFrame of features."""
    hashedString = b64Wav2string(wavPath)
    vectorisedFeatures = hashedString2Vec(hashedString)
    vectorisedList = convertVec2List(vectorisedFeatures)
    return convertList2Df(vectorisedList)




