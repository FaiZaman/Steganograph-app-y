# Steganograph-App-y

Welcome to Steganograph-App-y! This is a Python application where one can try out exisiting steganographic algorithms as well as different combinations of edge detectors for the purpose of embedding in steganography on an easy-to-use GUI.

## Getting Started

To get started with the app, first clone the repository and navigate to the directory:

```
git clone https://github.com/FaiZaman/Steganograph-app-y.git
cd Steganograph-app-y
```

## Running

To run the application, navigate to the root directory and run the following command:

```
python app.py
```

Note that your system must be running Python 3.7 or a later version for the application to function properly.

## Using the Graphical User Interface

Click `Embed`/`Hybrid Embed`/`Extract`/`Hybrid Extract` for these respective actions.

### Embedding

1) Select an embedding algorithm from the dropdown list.
2) Select the cover image file to embed a message into.
3) Select the message file to embed into the cover image.
4) Enter a secret key based on which the embedding order is determined (do not lose this key as it is needed for extraction!).
5) Select the folder where the stego image will be saved.
6) Click `Embed`.

### Hybrid Embedding

1) Select the first edge detector from the dropdown list.
2) Select the second edge detector from the dropdown list.
3) Select the hybridisation technique from the dropdown list.
4) Select the cover image file to embed a message into.
5) Select the message file to embed into the cover image.
6) Enter a secret key based on which the embedding order is determined (do not lose this key as it is needed for extraction!).
7) Select the folder where the stego image will be saved.
8) Click `Hybrid Embed`

### Extraction

1) Select an embedding algorithm from the dropdown list. This must be the same algorithm used to embed the message.
2) Select the stego image file to extract the message from.
3) Enter a secret key based on which the extraction order is determined. This must be the same key as the one used in the embedding process.
4) Select the folder where the extracted message will be saved.
5) Click `Extract`.

### Hybrid Extraction

1) Select the first edge detector from the dropdown list. This must be the same detector used in the embedding process.
2) Select the second edge detector from the dropdown list. This must be the same detector used in the embedding process.
3) Select the hybridisation technique from the dropdown list. This must be the same hybridisation technique used in the embedding process
4) Select the stego image file to extract the message from.
6) Enter a secret key based on which the extraction order is determined. This must be the same key as the one used in the embedding process.
7) Select the folder where the extracted message image will be saved.
8) Click `Hybrid Extract`.

## Credits

Credit to https://github.com/daniellerch/aletheia for the implementation of RS Analysis used for this project. Located in the project in the `aletheia` folder.

Credit to http://dde.binghamton.edu/ for the implementations of SPAM feature extractors and the Ensemble Classifier, both of which were used to evaluate the security of the schemes implemented. Located in the project in the `evaluation/features_classification` folder.