# WasteWise

WasteWise is an image-based waste classification app. It accepts up to five JPG or PNG images and classifies them into cardboard, glass, metal, paper, plastic, or trash.

The Python package contains the classifier interface, image validation and session logic, and the Streamlit UI. The demo classifier provides sample results for UI previews and does not analyze image contents. Model mode requires `models/trashnet_selected_model.keras` and `models/class_names.txt`. The class-name file is tracked in Git; model weights are ignored because they are large binary artifacts. Keep the weights locally in `models/`, or set `WASTEWISE_MODEL_DIR` to their location.

Set `WASTEWISE_MODE=demo` to run with sample preview results. The default mode is `model`.

## Run locally

Install dependencies with `python3 -m pip install -r requirements.txt`, then from
the directory containing this `wastewise/` folder run:

```sh
WASTEWISE_MODE=demo python3 -m streamlit run wastewise/app.py
```

Demo mode lets you preview the interface without the trained model. Model mode
requires the files described above. The upload panel includes an optional webcam
capture. Webcam access works on `localhost` or over HTTPS, and the browser will
ask for permission the first time.
