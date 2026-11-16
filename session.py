"""UI state and interaction rules (no Streamlit dependency).

One ``WasteWiseSession`` lives in ``st.session_state``. All rules about the
selection (5-image limit, stable IDs, clearing outdated results) live here so
they can be unit-tested without a browser.

Rule: any change to the selection (image added or removed) clears all results.
A batch is classified as a whole, so results never outlive the selection they
were produced for.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Iterable

from .classifier import ClassificationResult, Classifier, ClassifierUnavailableError
from .config import MAX_IMAGES
from .images import ImageRejected, SelectedImage, prepare_image

logger = logging.getLogger(__name__)

STATUS_IDLE = "idle"
STATUS_DONE = "done"
STATUS_ERROR = "error"


@dataclass
class WasteWiseSession:
    images: list[SelectedImage] = field(default_factory=list)
    results: dict[str, ClassificationResult] = field(default_factory=dict)
    status: str = STATUS_IDLE
    error: str | None = None
    notices: list[str] = field(default_factory=list)
    uploader_nonce: int = 0  # bumped to reset the upload widget after each ingest

    # ------------------------------------------------------------------ selection
    @property
    def is_full(self) -> bool:
        return len(self.images) >= MAX_IMAGES

    def add_files(self, files: Iterable[tuple[str, bytes]]) -> int:
        """Add uploaded files up to the limit. Returns how many were added."""
        self.notices = []
        added = 0
        over_limit = 0
        for name, data in files:
            if self.is_full:
                over_limit += 1
                continue
            try:
                self.images.append(prepare_image(name, data))
                added += 1
            except ImageRejected as exc:
                self.notices.append(f"{name} wasn’t added: {exc}.")
        if over_limit:
            noun = "image" if over_limit == 1 else "images"
            self.notices.append(
                f"Up to {MAX_IMAGES} images are allowed."
            )
        if added:
            self.clear_results()
        return added

    def remove(self, image_id: str) -> None:
        before = len(self.images)
        self.images = [img for img in self.images if img.id != image_id]
        self.notices = []
        if len(self.images) != before:
            self.clear_results()

    def clear_results(self) -> None:
        self.results = {}
        self.status = STATUS_IDLE
        self.error = None

    def clear_notices(self) -> None:
        self.notices = []

    def reset(self) -> None:
        """Start a fresh upload session and invalidate the uploader widget."""
        self.images = []
        self.notices = []
        self.clear_results()
        self.uploader_nonce += 1

    # --------------------------------------------------------------- classification
    def classify(
        self,
        classifier_factory: Callable[[], Classifier],
        on_progress: Callable[[int, int], None] | None = None,
    ) -> None:
        """Run the classifier over the current selection, one image at a time."""
        if not self.images:
            return
        self.clear_results()
        snapshot = list(self.images)
        results: dict[str, ClassificationResult] = {}
        try:
            classifier = classifier_factory()
            for done, img in enumerate(snapshot):
                if on_progress:
                    on_progress(done, len(snapshot))
                result = classifier.classify(img.id, img.data)
                if result.image_id != img.id:
                    raise RuntimeError("classifier returned a result for a different image")
                results[img.id] = result
            if on_progress:
                on_progress(len(snapshot), len(snapshot))
        except ClassifierUnavailableError as exc:
            self.status = STATUS_ERROR
            self.error = f"Classification isn’t available right now. {exc}"
        except Exception:  # noqa: BLE001 - surfaced to the user as a friendly message
            logger.exception("Classification failed")
            self.status = STATUS_ERROR
            self.error = "Something went wrong while classifying your images."
        else:
            self.results = results
            self.status = STATUS_DONE

    def result_entries(self) -> list[tuple[int, SelectedImage, ClassificationResult]]:
        """(position, image, result) for each selected image, in selection order.

        Pairing is done by stable image id, so a result can never be shown with
        a different image.
        """
        entries = []
        for pos, img in enumerate(self.images):
            result = self.results.get(img.id)
            if result is not None:
                entries.append((pos, img, result))
        return entries
