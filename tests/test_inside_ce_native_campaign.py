"""Tests for native-language site-scoped INSIDE CE campaign planner."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "inside_ce_native_campaign", ROOT / "scripts/build_inside_ce_native_search_campaign.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class NativeCECampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = module.load_tsv(module.DIRECTORY)
        cls.routes = module.load_tsv(module.ROUTES)
        cls.archives = module.load_tsv(module.ARCHIVES)
        cls.lexicon = module.load_tsv(module.LEXICON)

    def make_campaign(self, **kwargs):
        return module.build(
            self.directory, self.routes, self.archives, self.lexicon,
            allowed_statuses={"V", "C", "H"}, max_tasks=20000, **kwargs
        )

    def test_full_inventory_and_native_locale_coverage(self):
        self.assertEqual(len(self.directory), 483)
        self.assertEqual(len(self.lexicon), 50)
        tasks = self.make_campaign()
        self.assertGreater(len(tasks), 3000)
        self.assertEqual(len({t["task_id"] for t in tasks}), len(tasks))
        self.assertEqual(len({t["site"] for t in tasks}), 483)
        self.assertEqual({t["state"] for t in tasks}, {"planned_unexecuted"})

    def test_region_specific_native_formulations(self):
        tasks = self.make_campaign()
        examples = {
            "pt-BR": '"eu comprei"',
            "es-AR": '"me lo compré"',
            "zh-TW": '"貼紙"',
            "zh-HK": '"我買咗"',
            "ja": '"シール"',
            "ko": '"스티커"',
            "ar": '"الملصق"',
            "ru": '"наклейка"',
        }
        for loc, phrase in examples.items():
            self.assertTrue(any(t["locale"] == loc and phrase in t["expression"]
                                for t in tasks), loc)

    def test_native_site_matching_not_english_translate(self):
        tasks = self.make_campaign()
        for entry in tasks:
            allowed = module.locales_for_site(entry["site_language_label"])
            self.assertIn(entry["locale"], allowed)
            self.assertEqual(entry["archive_assurance"] != "", True)
            self.assertEqual(entry["host_capture_status"], "not_checked")
        # Test Thai posts use Thai source terms rather than English approximation.
        thai = [r for r in tasks if r["locale"] == "th"]
        self.assertTrue(any("สติกเกอร์" in r["expression"] for r in thai))

    def test_multilingual_global_and_bilingual_sites(self):
        self.assertIn("ur", module.locales_for_site("en-ur"))
        self.assertIn("en", module.locales_for_site("bn-en"))
        self.assertIn("si", module.locales_for_site("en-si"))
        self.assertIn("ne", module.locales_for_site("en-ne"))
        self.assertIn("zh-CN", module.locales_for_site("multi"))
        self.assertIn("fr", module.locales_for_site("ar-fr"))

    def test_bounded_and_category_filter(self):
        with self.assertRaises(ValueError):
            module.build(self.directory, self.routes, self.archives, self.lexicon,
                         allowed_statuses={"V","C","H"}, max_tasks=5)
        tasks = self.make_campaign(categories={"edition_number"})
        self.assertTrue(all(t["category"] == "edition_number" for t in tasks))
        self.assertTrue(all(t["expression"].count('"') >= 4 for t in tasks))

    def test_round_robin_not_only_english(self):
        tasks = self.make_campaign()
        first = {t["locale"] for t in tasks[:80]}
        self.assertIn("ja", first)
        self.assertIn("zh-TW", first)
        self.assertIn("pt-BR", first)
        self.assertIn("ar", first)
        self.assertTrue(any(x["site"] == "Gameblog Community" for x in tasks))

    def test_secondary_video_and_resale_leads(self):
        sources = module.load_tsv(module.SECONDARY)
        self.assertEqual(len(sources), 30)
        tasks = module.build_secondary(sources, self.lexicon)
        self.assertGreater(len(tasks), 300)
        self.assertEqual(len({x["site"] for x in tasks}), 30)
        self.assertTrue(all(x["state"] == "planned_unexecuted" for x in tasks))
        self.assertTrue(any(x["site"] == "YouTube" and x["locale"] == "ja"
                            for x in tasks))
        self.assertTrue(any(x["site"] == "Mercado Livre" and x["locale"] == "pt-BR"
                            for x in tasks))
        self.assertTrue(any(x["site"] == "Yahoo Auctions Japan" and x["locale"] == "ja"
                            for x in tasks))

    def test_full_native_lexicon_on_global_sources(self):
        expected = {x["locale"] for x in self.lexicon}
        self.assertEqual(set(module.MULTI_LOCALES), expected)
        forum_tasks = self.make_campaign()
        self.assertEqual(len(forum_tasks), 8940)
        social_tasks = module.build_secondary(module.load_tsv(module.SECONDARY), self.lexicon)
        self.assertEqual(len(social_tasks), 10755)
        self.assertEqual({x["locale"] for x in forum_tasks}, expected)
        self.assertEqual({x["locale"] for x in social_tasks}, expected)

    def test_small_paid_batch_is_multilingual_and_multisource(self):
        social_tasks = module.build_secondary(module.load_tsv(module.SECONDARY), self.lexicon)
        head = social_tasks[:20]
        self.assertGreaterEqual(len({x["locale"] for x in head}), 15)
        self.assertGreaterEqual(len({x["site"] for x in head}), 5)
        self.assertEqual({x["state"] for x in head}, {"planned_unexecuted"})

    def test_rejects_mismatched_archive_rows(self):
        archives = [dict(x) for x in self.archives]
        archives[0]["community"] = "WRONG"
        with self.assertRaises(ValueError):
            module.build(self.directory, self.routes, archives, self.lexicon,
                         allowed_statuses={"V","C","H"}, max_tasks=20000)

if __name__ == "__main__":
    unittest.main()
