"""Unit tests for scripts/validate_posts.py."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_posts import validate


class ValidatePostsTests(unittest.TestCase):
    def validate_value(self, value: object) -> list[str]:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "posts.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            return validate(path)

    def test_accepts_required_fields_without_optional_sources(self) -> None:
        post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check"}

        self.assertEqual(self.validate_value([post]), [])

    def test_accepts_optional_http_and_https_sources(self) -> None:
        post = {
            "id": 1,
            "n": 2,
            "c": 3,
            "t": "Claim",
            "v": "Check",
            "s": ["https://example.com/source", "http://example.org/report"],
        }

        self.assertEqual(self.validate_value([post]), [])

    def test_accepts_optional_errata(self) -> None:
        post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check", "e": "Corrected year."}

        self.assertEqual(self.validate_value([post]), [])

    def test_rejects_empty_errata(self) -> None:
        for errata in ("", " \t\n"):
            with self.subTest(errata=errata):
                post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check", "e": errata}

                errors = self.validate_value([post])

                self.assertTrue(any("[0].e:" in error for error in errors))

    def test_rejects_non_string_errata(self) -> None:
        for errata in (None, 42, True, [], {}):
            with self.subTest(errata=errata):
                post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check", "e": errata}

                errors = self.validate_value([post])

                self.assertTrue(any("[0].e:" in error for error in errors))

    def test_accepts_optional_time_and_topic(self) -> None:
        post = {"id": 1, "n": 1, "c": 1, "h": "21:34", "a": "Economia", "t": "Claim", "v": "Check"}

        self.assertEqual(self.validate_value([post]), [])

    def test_rejects_non_string_time_or_topic(self) -> None:
        for field in ("h", "a"):
            with self.subTest(field=field):
                post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check"}
                post[field] = 2134
                errors = self.validate_value([post])

                self.assertTrue(any(f"[0].{field}:" in error for error in errors))

    def test_accepts_empty_feed_and_unrecognized_extra_fields(self) -> None:
        post = {"id": 1, "n": 1, "c": 2, "t": "Claim", "v": "Check", "future": True}

        self.assertEqual(self.validate_value([]), [])
        self.assertEqual(self.validate_value([post]), [])

    def test_rejects_non_array_root_and_non_object_entries(self) -> None:
        root_errors = self.validate_value({})
        entry_errors = self.validate_value([None])

        self.assertTrue(any("top-level value must be an array" in error for error in root_errors))
        self.assertTrue(any("each post must be an object" in error for error in entry_errors))

    def test_requires_id_n_c_t_and_v(self) -> None:
        for field in ("id", "n", "c", "t", "v"):
            with self.subTest(field=field):
                post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check"}
                del post[field]

                errors = self.validate_value([post])

                self.assertTrue(any(f"[0].{field}:" in error for error in errors))

    def test_rejects_invalid_or_repeated_ids(self) -> None:
        for post_id in (0, -1, "1", True, 1.5):
            with self.subTest(id=post_id):
                post = {"id": post_id, "n": 1, "c": 1, "t": "Claim", "v": "Check"}
                self.assertTrue(self.validate_value([post]))

        post = {"id": 7, "n": 1, "c": 1, "t": "Claim", "v": "Check"}
        errors = self.validate_value([post, dict(post)])
        self.assertEqual(len(errors), 1)
        self.assertIn("[1].id:", errors[0])

    def test_rejects_unknown_candidate_and_check_values(self) -> None:
        for field, value in (("n", 3), ("c", 5), ("c", -1)):
            with self.subTest(field=field, value=value):
                post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check"}
                post[field] = value
                self.assertTrue(self.validate_value([post]))

    def test_accepts_no_verdict_seals_without_sources(self) -> None:
        # 0 (em verificação) and 4 (não verificável) carry no verdict, so no source is required
        for check, label in ((0, "em_verificacao"), (4, "nao_verificavel")):
            with self.subTest(c=check):
                post = {"id": 1, "n": 2, "c": check, "r": label, "t": "Claim", "v": "Check"}
                self.assertEqual(self.validate_value([post]), [])

    def test_detailed_label_must_match_its_seal(self) -> None:
        good = {"id": 1, "n": 1, "c": 3, "r": "exagerado", "t": "Claim", "v": "Check", "s": ["https://example.com"]}
        self.assertEqual(self.validate_value([good]), [])

        for label, check in (("exagerado", 2), ("falso", 3), ("verdadeiro", 2), ("insustentavel", 1)):
            with self.subTest(r=label, c=check):
                post = dict(good, r=label, c=check)
                errors = self.validate_value([post])
                self.assertTrue(any("[0].r:" in error for error in errors))

        for label in ("", "parcial", 3, None):
            with self.subTest(r=label):
                post = dict(good, r=label)
                errors = self.validate_value([post])
                self.assertTrue(any("[0].r:" in error for error in errors))

    def test_new_scheme_verdict_requires_a_source(self) -> None:
        for check, label in ((1, "verdadeiro"), (2, "falso"), (3, "falta_contexto")):
            with self.subTest(c=check):
                post = {"id": 1, "n": 1, "c": check, "r": label, "t": "Claim", "v": "Check"}
                errors = self.validate_value([post])
                self.assertTrue(any("[0].s:" in error for error in errors))

                post["s"] = ["https://example.com/data"]
                self.assertEqual(self.validate_value([post]), [])

    def test_legacy_verdict_without_source_is_only_a_warning(self) -> None:
        from scripts.validate_posts import check

        post = {"id": 1, "n": 1, "c": 2, "t": "Claim", "v": "Check"}
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "posts.json"
            path.write_text(json.dumps([post]), encoding="utf-8")
            errors, warnings = check(path)

        self.assertEqual(errors, [])
        self.assertTrue(any("[0].s:" in warning for warning in warnings))

    def test_accepts_history_and_reviewers(self) -> None:
        post = {
            "id": 1,
            "n": 2,
            "c": 3,
            "r": "falta_contexto",
            "t": "Claim",
            "v": "Check",
            "s": ["https://example.com"],
            "hist": [{"de": "parcial", "para": "falta_contexto", "quando": "2026-10-23T23:12-03:00", "motivo": "fonte"}],
            "chk": ["@a", "@b"],
        }
        self.assertEqual(self.validate_value([post]), [])

    def test_accepts_review_trail_and_other_agencies(self) -> None:
        post = {
            "id": 1, "n": 1, "c": 3, "r": "exagerado", "t": "Claim", "v": "Check", "s": ["https://example.com"],
            "v0": "Texto original", "c0": 2,
            "outras": [{"agencia": "Lupa", "rotulo": "Exagerado", "url": "https://example.org/check"}, {"agencia": "Aos Fatos"}],
        }
        self.assertEqual(self.validate_value([post]), [])

    def test_rejects_malformed_review_trail_and_other_agencies(self) -> None:
        base = {"id": 1, "n": 1, "c": 3, "r": "exagerado", "t": "Claim", "v": "Check", "s": ["https://example.com"]}
        for field, value in (("v0", ""), ("v0", 3), ("c0", 7), ("c0", "2"), ("outras", "Lupa"), ("outras", [{}]),
                             ("outras", [{"agencia": ""}]), ("outras", [{"agencia": "Lupa", "url": "javascript:x"}]),
                             ("outras", [{"agencia": "Lupa", "rotulo": " "}])):
            with self.subTest(field=field, value=value):
                post = dict(base)
                post[field] = value
                errors = self.validate_value([post])
                self.assertTrue(any(f"[0].{field}" in error for error in errors))

    def test_rejects_malformed_history_reviewers_and_ai_flag(self) -> None:
        base = {"id": 1, "n": 2, "c": 3, "r": "falta_contexto", "t": "Claim", "v": "Check", "s": ["https://example.com"]}
        bad_values = (
            ("hist", "not a list"),
            ("hist", [None]),
            ("hist", [{"de": "parcial"}]),
            ("hist", [{"de": "", "para": "falso"}]),
            ("hist", [{"de": "parcial", "para": "falso", "quando": ""}]),
            ("chk", []),
            ("chk", ["@a", ""]),
            ("chk", "@a"),
        )
        for field, value in bad_values:
            with self.subTest(field=field, value=value):
                post = dict(base)
                post[field] = value
                errors = self.validate_value([post])
                self.assertTrue(any(f"[0].{field}" in error for error in errors))

    def test_rejects_boolean_as_candidate_or_check_number(self) -> None:
        for field in ("n", "c"):
            with self.subTest(field=field):
                post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check"}
                post[field] = True
                self.assertTrue(self.validate_value([post]))

    def test_rejects_non_string_claim_or_verification(self) -> None:
        for field in ("t", "v"):
            with self.subTest(field=field):
                post = {"id": 1, "n": 1, "c": 1, "t": "Claim", "v": "Check"}
                post[field] = 42
                self.assertTrue(self.validate_value([post]))

    def test_optional_sources_must_be_an_array_of_valid_http_urls(self) -> None:
        invalid_sources = (
            "https://example.com",
            ["javascript:alert(1)"],
            ["https://"],
            ["https://example.com:99999/path"],
            [42],
        )
        for sources in invalid_sources:
            with self.subTest(sources=sources):
                post = {
                    "id": 1,
                    "n": 1,
                    "c": 1,
                    "t": "Claim",
                    "v": "Check",
                    "s": sources,
                }
                self.assertTrue(self.validate_value([post]))

    def test_rejects_invalid_json_constants(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / "posts.json"
            path.write_text("[NaN]", encoding="utf-8")

            errors = validate(path)

        self.assertTrue(any("could not read valid JSON" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
