import unittest

from models.rfm import build_rfm_table
from preprocessing.data_pipeline import PipelineConfig, generate_synthetic_transactions, preprocess_transactions
from recommendation.engine import popularity_based_recommendations


class TestCustomerBehaviorPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = generate_synthetic_transactions(PipelineConfig(n_records=1500, random_seed=7))
        cls.processed = preprocess_transactions(raw)

    def test_required_columns_exist_after_preprocessing(self):
        expected = {
            "customer_id",
            "transaction_id",
            "product_category",
            "purchase_amount",
            "purchase_date",
            "payment_method",
            "city",
            "gender",
            "age",
            "quantity",
            "frequency",
            "recency",
            "revenue",
            "month",
            "age_group",
        }
        self.assertTrue(expected.issubset(set(self.processed.columns)))

    def test_rfm_segmentation_outputs_labels(self):
        rfm = build_rfm_table(self.processed)
        self.assertIn("rfm_segment", rfm.columns)
        self.assertGreater(len(rfm["rfm_segment"].unique()), 1)

    def test_recommendations_return_ranked_categories(self):
        customer_id = int(self.processed["customer_id"].iloc[0])
        recs = popularity_based_recommendations(self.processed, customer_id, top_n=3)
        self.assertLessEqual(len(recs), 3)
        self.assertTrue(all(isinstance(item, str) for item in recs))


if __name__ == "__main__":
    unittest.main()
