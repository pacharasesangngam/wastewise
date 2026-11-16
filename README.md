# WasteWise

WasteWise is an image-based waste classification app. It accepts up to five JPG or PNG images and classifies them into cardboard, glass, metal, paper, plastic, or trash.

The Python package contains the trained MobileNetV2 classifier, image validation and session logic, and the Streamlit UI. The app uses the real model by default. Demo mode is available only for UI previews and does not analyze image contents. Model mode requires `models/trashnet_selected_model.keras` and `models/class_names.txt`. The class-name file is tracked in Git; model weights are ignored because they are large binary artifacts. Keep the weights locally in `models/`, or set `WASTEWISE_MODEL_DIR` to their location.

Set `WASTEWISE_MODE=demo` to run with sample preview results. The default mode is `model`.

## Run locally

Install dependencies with `python3 -m pip install -r wastewise/requirements.txt`, then from
the directory containing this `wastewise/` folder run:

```sh
python3 -m streamlit run wastewise/app.py
```

To preview the interface with sample (non-predictive) results, run with
`WASTEWISE_MODE=demo`. Real model mode requires the files described above. The
upload panel includes an optional webcam capture. Webcam access works on
`localhost` or over HTTPS, and the browser will ask for permission the first time.
