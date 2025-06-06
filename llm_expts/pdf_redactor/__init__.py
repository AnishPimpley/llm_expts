"""Utility functions for redacting PDF files."""

from __future__ import annotations

import fitz  # PyMuPDF


def identify_redactable_substrings(text: str) -> list[str]:
    """Identify parts of ``text`` that should be redacted.

    This placeholder implementation simply redacts any word that is entirely
    numeric.  It can be replaced with more sophisticated logic if needed.
    """
    words = text.split()
    numbers = {word for word in words if word.isdigit()}
    return sorted(numbers)


def redact_pdf(input_path: str, output_path: str) -> None:
    """Redact the given PDF and write the result to ``output_path``.

    Parameters
    ----------
    input_path:
        Path to the PDF that should be processed.
    output_path:
        Path where the redacted PDF should be written.
    """

    document = fitz.open(input_path)
    for page in document:
        text = page.get_text()
        substrings = identify_redactable_substrings(text)
        for substring in substrings:
            for inst in page.search_for(substring):
                page.add_redact_annot(inst, fill=(0, 0, 0))
        page.apply_redactions()

    document.save(output_path, garbage=4, deflate=True)
