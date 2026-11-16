"""Tests for everything that does not need a running Streamlit app.

Run from the project root:   python -m unittest discover -s tests -v
"""

import io
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

# This checkout is itself the ``wastewise`` package, so imports need its parent.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from PIL import Image  # noqa: E402

from wastewise import classifier, config, images  # noqa: E402
from wastewise.classifier import (  # noqa: E402
    ClassificationResult,
    ClassifierUnavailableError,
    DemoClassifier,
    TrainedModelClassifier,
    get_classifier,
)
from wastewise.guidance import GUIDANCE  # noqa: E402
from wastewise.session import (  # noqa: E402
    STATUS_DONE,
    STATUS_ERROR,
    STATUS_IDLE,
    WasteWiseSession,
)
from wastewise.ui import html, icons, theme  # noqa: E402


def make_image(fmt="PNG", color=(10, 120, 60), size=(64, 48), mode="RGB") -> bytes:
    buf = io.BytesIO()
    Image.new(mode, size, color).save(buf, format=fmt)
    return buf.getvalue()


def files(n, ext="png", fmt="PNG"):
    # Different colours so each file has different bytes.
    return [(f"item{i}.{ext}", make_image(fmt, (i * 30, 100, 50))) for i in range(n)]


def demo_factory():
    return DemoClassifier(delay_seconds=0)


class PredictingModel:
    def __init__(self):
        self.batches = []

    def predict(self, batch, verbose=0):
        self.batches.append(batch.copy())
        return [[1 / 6] * len(config.CLASS_LABELS)]


class GuidanceTests(unittest.TestCase):
    def test_covers_exactly_the_six_classes(self):
        self.assertEqual(tuple(GUIDANCE), config.CLASS_LABELS)
        self.assertEqual(len(GUIDANCE), 6)

    def test_every_entry_is_complete_and_icons_exist(self):
        for key, g in GUIDANCE.items():
            self.assertEqual(g.key, key)
            for field in ("name_en", "name_th", "bin_en", "bin_th", "instructions_en", "instructions_th", "accent"):
                self.assertTrue(getattr(g, field).strip(), f"{key}.{field} empty")
            self.assertIn(g.material_icon, icons.names())
            self.assertIn(g.bin_icon, icons.names())


class ClassifierTests(unittest.TestCase):
    def test_ranked_sorted_descending_and_predicted_is_top(self):
        scores = {"cardboard": 0.1, "glass": 0.05, "metal": 0.15, "paper": 0.2, "plastic": 0.4, "trash": 0.1}
        r = ClassificationResult("x", scores, is_demo=False)
        vals = [s for _, s in r.ranked()]
        self.assertEqual(vals, sorted(vals, reverse=True))
        self.assertEqual(r.predicted, "plastic")
        self.assertAlmostEqual(r.confidence, 0.4)
        self.assertEqual(len(r.ranked()), 6)

    def test_ties_keep_label_order(self):
        scores = {label: 1 / 6 for label in config.CLASS_LABELS}
        r = ClassificationResult("x", scores, is_demo=False)
        self.assertEqual([l for l, _ in r.ranked()], list(config.CLASS_LABELS))

    def test_demo_is_flagged_deterministic_and_normalised(self):
        data = make_image()
        a = DemoClassifier(0).classify("id1", data)
        b = DemoClassifier(0).classify("id1", data)
        self.assertTrue(a.is_demo)
        self.assertEqual(a.scores, b.scores)
        self.assertAlmostEqual(sum(a.scores.values()), 1.0)
        self.assertEqual(set(a.scores), set(config.CLASS_LABELS))

    def test_trained_model_stub_is_unavailable_not_fake(self):
        with self.assertRaises(ClassifierUnavailableError):
            TrainedModelClassifier().classify("id", b"x")

    def test_get_classifier_modes(self):
        self.assertTrue(get_classifier("demo").is_demo)
        with patch.object(classifier, "TrainedModelClassifier") as trained:
            trained.return_value.is_demo = False
            self.assertFalse(get_classifier("model").is_demo)
        with self.assertRaises(ClassifierUnavailableError):
            get_classifier("nonsense")


class ImageTests(unittest.TestCase):
    def test_accepts_png_jpg_jpeg(self):
        for ext, fmt in (("png", "PNG"), ("jpg", "JPEG"), ("jpeg", "JPEG"), ("JPG", "JPEG")):
            img = images.prepare_image(f"a.{ext}", make_image(fmt))
            self.assertTrue(img.thumb_b64)
            self.assertTrue(img.preview)

    def test_transparent_png_is_accepted(self):
        data = make_image("PNG", (0, 0, 0, 0), mode="RGBA")
        self.assertTrue(images.prepare_image("t.png", data).preview)

    def test_rejections(self):
        with self.assertRaises(images.ImageRejected):
            images.prepare_image("a.gif", make_image("PNG"))
        with self.assertRaises(images.ImageRejected):
            images.prepare_image("a.png", b"")
        with self.assertRaises(images.ImageRejected):
            images.prepare_image("a.png", b"not an image at all")
        with self.assertRaises(images.ImageRejected):
            images.prepare_image("noext", make_image("PNG"))

    def test_size_limit(self):
        original = images.MAX_FILE_BYTES
        images.MAX_FILE_BYTES = 100
        try:
            with self.assertRaises(images.ImageRejected) as cm:
                images.prepare_image("a.png", make_image("PNG", size=(200, 200)))
            self.assertIn("200MB", str(cm.exception))
        finally:
            images.MAX_FILE_BYTES = original
        self.assertEqual(config.MAX_FILE_BYTES, 200 * 1024 * 1024)

    def test_large_image_preview_is_downscaled(self):
        img = images.prepare_image("big.png", make_image("PNG", size=(3000, 2000)))
        w, h = Image.open(io.BytesIO(img.preview)).size
        self.assertLessEqual(max(w, h), images.PREVIEW_MAX_PX)


class SessionSelectionTests(unittest.TestCase):
    def test_upload_does_not_classify(self):
        s = WasteWiseSession()
        s.add_files(files(2))
        self.assertEqual(len(s.images), 2)
        self.assertEqual(s.status, STATUS_IDLE)
        self.assertEqual(s.results, {})

    def test_five_image_limit_in_one_batch(self):
        s = WasteWiseSession()
        added = s.add_files(files(7))
        self.assertEqual(added, 5)
        self.assertEqual(len(s.images), 5)
        self.assertTrue(s.is_full)
        self.assertTrue(any("Up to 5 images are allowed" in n for n in s.notices))

    def test_five_image_limit_across_batches(self):
        s = WasteWiseSession()
        s.add_files(files(3))
        s.add_files(files(3))
        self.assertEqual(len(s.images), 5)
        self.assertTrue(any("Up to 5 images are allowed" in n for n in s.notices))
        self.assertEqual(s.add_files(files(1)), 0)
        self.assertEqual(len(s.images), 5)

    def test_remove_then_add_replacement(self):
        s = WasteWiseSession()
        s.add_files(files(5))
        self.assertTrue(s.is_full)
        removed = s.images[2].id
        s.remove(removed)
        self.assertEqual(len(s.images), 4)
        self.assertFalse(s.is_full)
        self.assertNotIn(removed, [i.id for i in s.images])
        s.add_files(files(1, ext="jpg", fmt="JPEG"))
        self.assertEqual(len(s.images), 5)

    def test_ids_are_unique_and_never_reused(self):
        s = WasteWiseSession()
        s.add_files(files(5))
        seen = {i.id for i in s.images}
        self.assertEqual(len(seen), 5)
        s.remove(s.images[0].id)
        s.add_files(files(1))
        self.assertEqual(len({i.id for i in s.images}), 5)
        self.assertEqual(len(seen | {i.id for i in s.images}), 6)

    def test_same_file_twice_gets_distinct_ids(self):
        s = WasteWiseSession()
        data = make_image()
        s.add_files([("a.png", data), ("a.png", data)])
        self.assertEqual(len({i.id for i in s.images}), 2)

    def test_rejected_files_are_reported_and_do_not_count(self):
        s = WasteWiseSession()
        s.add_files([("bad.png", b"junk"), ("ok.png", make_image()), ("x.gif", make_image())])
        self.assertEqual(len(s.images), 1)
        self.assertEqual(len(s.notices), 2)

    def test_remove_unknown_id_is_harmless(self):
        s = WasteWiseSession()
        s.add_files(files(2))
        s.remove("does-not-exist")
        self.assertEqual(len(s.images), 2)

    def test_reset_starts_a_fresh_upload_session(self):
        s = WasteWiseSession()
        s.add_files(files(2))
        s.classify(demo_factory)
        nonce = s.uploader_nonce
        s.reset()
        self.assertEqual(s.images, [])
        self.assertEqual(s.results, {})
        self.assertEqual(s.status, STATUS_IDLE)
        self.assertEqual(s.notices, [])
        self.assertEqual(s.uploader_nonce, nonce + 1)


class SessionClassificationTests(unittest.TestCase):
    def setUp(self):
        self.s = WasteWiseSession()
        self.s.add_files(files(3))

    def test_classify_produces_result_per_image_in_order(self):
        progress = []
        self.s.classify(demo_factory, lambda d, t: progress.append((d, t)))
        self.assertEqual(self.s.status, STATUS_DONE)
        entries = self.s.result_entries()
        self.assertEqual([p for p, _, _ in entries], [0, 1, 2])
        for _, img, res in entries:
            self.assertEqual(img.id, res.image_id)
            self.assertTrue(res.is_demo)
        self.assertEqual(progress[0], (0, 3))
        self.assertEqual(progress[-1], (3, 3))

    def test_classify_with_no_images_does_nothing(self):
        s = WasteWiseSession()
        s.classify(demo_factory)
        self.assertEqual(s.status, STATUS_IDLE)

    def test_results_cleared_when_image_removed(self):
        self.s.classify(demo_factory)
        self.s.remove(self.s.images[1].id)
        self.assertEqual(self.s.status, STATUS_IDLE)
        self.assertEqual(self.s.results, {})
        self.assertEqual(self.s.result_entries(), [])

    def test_results_cleared_when_image_added(self):
        self.s.classify(demo_factory)
        self.s.add_files(files(1, ext="jpg", fmt="JPEG"))
        self.assertEqual(self.s.status, STATUS_IDLE)
        self.assertEqual(self.s.results, {})

    def test_rejected_upload_keeps_existing_results(self):
        self.s.classify(demo_factory)
        self.s.add_files([("bad.png", b"junk")])
        self.assertEqual(self.s.status, STATUS_DONE)
        self.assertEqual(len(self.s.result_entries()), 3)

    def test_over_limit_upload_keeps_results_when_nothing_added(self):
        s = WasteWiseSession()
        s.add_files(files(5))
        s.classify(demo_factory)
        s.add_files(files(2))
        self.assertEqual(s.status, STATUS_DONE)

    def test_result_pairing_uses_ids_not_positions(self):
        self.s.classify(demo_factory)
        # Simulate a reorder: results must still follow their own image.
        self.s.images.reverse()
        for _, img, res in self.s.result_entries():
            self.assertEqual(img.id, res.image_id)

    def test_trained_model_classifies_the_selected_images(self):
        with patch.object(classifier, "_load_model", return_value=PredictingModel()), patch.object(
            classifier, "_load_class_labels", return_value=config.CLASS_LABELS
        ):
            self.s.classify(lambda: get_classifier("model"))
        self.assertEqual(self.s.status, STATUS_DONE)
        self.assertEqual(len(self.s.results), 3)
        for result in self.s.results.values():
            self.assertFalse(result.is_demo)
            self.assertEqual(tuple(result.scores), config.CLASS_LABELS)
            self.assertAlmostEqual(sum(result.scores.values()), 1.0, places=5)

    def test_trained_model_uses_training_input_scale(self):
        model = PredictingModel()
        with patch.object(classifier, "_load_model", return_value=model), patch.object(
            classifier, "_load_class_labels", return_value=config.CLASS_LABELS
        ):
            trained = get_classifier("model")
            image = images.prepare_image("bottle.png", make_image("PNG", color=(30, 120, 200)))
            result = trained.classify(image.id, image.data)
        self.assertEqual(tuple(result.scores), config.CLASS_LABELS)
        self.assertTrue(all(0.0 <= score <= 1.0 for score in result.scores.values()))
        batch = model.batches[0]
        self.assertEqual(batch.shape, (1, 224, 224, 3))
        self.assertAlmostEqual(float(batch[0, 0, 0, 0]), 30 / 255, places=4)
        self.assertAlmostEqual(float(batch[0, 0, 0, 1]), 120 / 255, places=4)
        self.assertAlmostEqual(float(batch[0, 0, 0, 2]), 200 / 255, places=4)

    def test_unexpected_failure_is_friendly_and_leaks_nothing(self):
        class Boom:
            name, is_demo = "boom", False

            def classify(self, image_id, image_bytes):
                raise ValueError("secret internal detail /srv/model.pt")

        self.s.classify(lambda: Boom())
        self.assertEqual(self.s.status, STATUS_ERROR)
        self.assertNotIn("secret", self.s.error)
        self.assertNotIn("model.pt", self.s.error)

    def test_result_for_wrong_image_is_rejected(self):
        class Wrong:
            name, is_demo = "wrong", True

            def classify(self, image_id, image_bytes):
                return ClassificationResult("someone-else", {l: 1 / 6 for l in config.CLASS_LABELS}, True)

        self.s.classify(lambda: Wrong())
        self.assertEqual(self.s.status, STATUS_ERROR)
        self.assertEqual(self.s.results, {})

    def test_error_then_retry_succeeds(self):
        def unavailable_factory():
            raise ClassifierUnavailableError("model unavailable")

        self.s.classify(unavailable_factory)
        self.s.classify(demo_factory)
        self.assertEqual(self.s.status, STATUS_DONE)
        self.assertIsNone(self.s.error)


class HtmlAndThemeTests(unittest.TestCase):
    def _result(self):
        return DemoClassifier(0).classify("abc", make_image())

    def _assert_markdown_safe(self, s):
        self.assertNotIn("\n", s)
        self.assertFalse(s.startswith(" "))
        ET.fromstring(f"<root>{s}</root>")  # well-formed

    def test_fragments_are_single_line_and_well_formed(self):
        s = WasteWiseSession()
        s.add_files(files(1))
        res = self._result()
        for frag in (
            html.header_html(True),
            html.header_html(False),
            html.count_html(2),
            html.thumb_html(s.images[0]),
            html.notices_html(["a & b"]),
            html.empty_state_html(0),
            html.empty_state_html(3),
            html.error_state_html("Oops <b>"),
            html.result_html(res),
            html.scores_html(res),
        ):
            self._assert_markdown_safe(frag)

    def test_demo_is_labelled_everywhere(self):
        res = self._result()
        self.assertNotIn("Sample results for previewing the layout", html.header_html(True))
        self.assertNotIn("Demo mode", html.header_html(False))
        out = html.result_html(res)
        self.assertIn("Demo mode", out)
        self.assertIn("Sample confidence (demo)", out)

    def test_real_result_is_not_labelled_demo(self):
        res = ClassificationResult("x", {**{l: 0.0 for l in config.CLASS_LABELS}, "glass": 1.0}, is_demo=False)
        out = html.result_html(res)
        self.assertNotIn("Demo", out)
        self.assertIn("Model confidence", out)
        self.assertIn("not the model’s overall accuracy", out)

    def test_result_shows_thai_and_english_and_bin(self):
        res = ClassificationResult("x", {**{l: 0.0 for l in config.CLASS_LABELS}, "glass": 1.0}, is_demo=False)
        out = html.result_html(res)
        for text in ("Glass", "แก้ว", "Recyclable waste bin", "ถังขยะรีไซเคิล", "Recommended bin"):
            self.assertIn(text, out)

    def test_scores_list_all_six_sorted_with_top_highlighted(self):
        res = self._result()
        out = html.scores_html(res)
        self.assertEqual(len(re.findall(r'class="ww-score(?: is-top)?"', out)), 6)
        self.assertEqual(out.count("is-top"), 1)
        names = [GUIDANCE[l].name_en for l, _ in res.ranked()]
        positions = [out.index(n) for n in names]
        self.assertEqual(positions, sorted(positions))
        self.assertTrue(out.index("is-top") < out.index(names[1]))

    def test_user_text_is_escaped(self):
        s = WasteWiseSession()
        s.add_files([('<script>alert(1)</script>.png', make_image())])
        out = html.thumb_html(s.images[0])
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;script&gt;", out)
        self.assertNotIn("<b>", html.error_state_html("<b>x</b>"))

    def test_icons_are_valid_svg(self):
        for name in icons.names():
            ET.fromstring(icons.svg(name))

    def test_css_is_one_line_with_palette_font_and_upload_texts(self):
        css = theme.style_tag()
        self.assertNotIn("\n", css)
        for token in ("#14232F", "#DCE3E8", "#EEF2F4", "#F2C230", "IBM Plex Sans Thai", "family=Bricolage+Grotesque"):
            self.assertIn(token, css)
        self.assertIn('content:"Add up to 5 photos"', css)
        self.assertIn('content:"JPG or PNG, up to 200MB each"', css)
        for placeholder in ("__GREEN__", "__SAGE__", "__CREAM__", "__DEEP__", "__PLUS__", "__MAX__", "__LIMIT__"):
            self.assertNotIn(placeholder, css)


if __name__ == "__main__":
    unittest.main()
