# Academic provenance and later improvements

This project originated as an individual university Python programming assignment in Principles of Programming II (2024). The source was recovered from the submitted assignment archive and previously verified against that archive. The current program includes later improvements; it is not byte-for-byte identical to the original submission.

The original approach greedily packed descending cut lengths into four-metre rods. Later improvements:

- Report the number of rods actually used rather than a potentially unattainable total-length lower bound.
- Expose a validated, nonmutating `build_cut_plan` function for testing.
- Use Decimal arithmetic and parse console lengths directly as Decimal.
- Reject nonfinite and out-of-range input and handle end-of-input cleanly.
- Add regression tests, small-instance oracle comparisons and an explicit non-optimality example.
- Clarify setup, assumptions and limitations.

No original collaborators have been identified. The author has confirmed individual ownership and university publication permission. This repository does not include assignment papers, marking rubrics, original reports, grades, student identifiers, university records or other course materials. It contains no bundled third-party libraries or media assets.

Preparation and subsequent fixes/tests were assisted by AI coding tools. This statement does not imply that the original submitted work used those tools, or that the later fixes were part of the submission.

The public author credit appears in README.md. Licensing remains undecided; no open-source license is declared.
