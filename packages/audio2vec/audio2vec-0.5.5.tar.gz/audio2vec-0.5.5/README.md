# Audio2Vector: Audio to Vector Conversion Package

## Description

Audio2Vec is a Python package designed to convert audio data into vector representations. This package is useful for various applications in machine learning and data analysis where audio data needs to be processed and analyzed.

## Features

- **Audio Processing**: Convert audio files into a format suitable for data analysis and machine learning.
- **Vector Conversion**: Transform processed audio data into vector representations.
- **Compatibility**: Works with wav audio file format (.wav)

## Installation

You can install Audio2Vector via pip:

```
pip install audio2vec

## Usage

from audio2vec import Audio2Vec

# Initialize the processor
processor = Audio2Vec()

or

# Define the number of Dimensions/Feature you want from the audio string
precessor = Audio2Vec(n_features=7)


# Load the audio to be converted to vector and stored in a DF
audioDataDF = processor.audio2Vec2DfProcessor('path_to_your_audio_file.wav')

# Convert audio to Python-list
audioDataList = processor.audio2ListProcessor('path_to_your_audio_file.wav')

# convert audio to raw Vectors
audioDataVector = processor.audio2VectorProcessor('path_to_your_audio_file.wav')

# Now you can use the vector for further analysis
```

## Contributing
Contributions are welcome! Please read the contributing guidelines before starting.

# Contributing Guidelines for Audio2Vector

First off, thank you for considering contributing to Audio2Vector. It's people like you that make Audio2Vector such a great tool.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our Issues if there's something similar to what you have in mind. If there isn't, feel free to open a new issue!

## Fork & create a branch

If this is something you think you can fix, then fork Audio2Vector and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):
```
git checkout -b 325-conversion-enhancement
```
Implement your fix or feature
At this point, you’re ready to make your changes! Feel free to ask for help; everyone is a beginner at first.

## Make a Pull Request
At this point, you should switch back to your master branch and make sure it’s up to date with Audio2Vector’s master branch:

```git remote add upstream git@github.com:yourusername/Audio2Vector.git```

```git checkout master```

```git pull upstream master```

Then update your feature branch from your local copy of master and push your update to your fork:

```git checkout 325-conversion-enhancement```

```git rebase master```

```git push --set-upstream origin 325-conversion-enhancement```

###### And submit a Pull Request with your changes.

## Keeping your Pull Request updated
If a maintainer asks you to “rebase” your PR, they’re saying that a lot of code has changed, and that you need to update your branch so it’s easier to merge.

To learn more about rebasing in Git, there are a lot of good resources but here’s the suggested workflow:

```git checkout 325-conversion-enhancement```

```git pull --rebase upstream master```

```git push --force-with-lease 325-conversion-enhancement```

## Merging a PR (maintainers only)
* A PR can only be merged into master by a maintainer if:

* It is passing CI.

* It has been approved by at least two maintainers. If it was a maintainer who opened the PR, only one extra approval is needed.

* It has no requested changes.

* It is up-to-date with current master.

* Any maintainer is allowed to merge a PR if all of these conditions are met.


## License
This project is licensed under the terms of the MIT license.

## Contact
If you have any questions, feel free to reach out or open an issue. cwakhusama@gmail.com or https://github.com/dallo7/audio2Vec

Please replace `'path_to_your_audio_file'` with the actual path to your audio file. Also, make sure to replace the example code and other details with the actual details of your package.



