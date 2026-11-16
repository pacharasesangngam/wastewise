# WasteWise

WasteWise is an image-based waste classification app. It accepts up to five JPG or PNG images and classifies them into cardboard, glass, metal, paper, plastic, or trash.

The Python package contains the classifier interface, image validation and session logic, and the Streamlit UI. The demo classifier provides sample results for UI previews and does not analyze image contents. Model mode requires the trained Keras model and class-name file under `models/`.

Set `WASTEWISE_MODE=demo` to run with sample preview results. The default mode is `model`.
