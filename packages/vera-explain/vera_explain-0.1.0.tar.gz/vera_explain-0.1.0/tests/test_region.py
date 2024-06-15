import unittest

import numpy as np
import pandas as pd

import vera


class TestIntersectWithOther(unittest.TestCase):
    def test_construct_region_with_single_hole(self):
        np.random.seed(0)

        x = np.random.uniform(-1, 1, size=(500, 2))

        features = pd.DataFrame()
        features["inner"] = np.linalg.norm(x, axis=1) < 0.5

        # The function returns the base variables, of which there should only be one
        region_annotations = vera.an.generate_region_annotations(
            features, embedding=x, scale_factor=0.5, sample_size=None,
        )
        self.assertEqual(
            1,
            len(region_annotations),
            "`an.generate_explanatory_features` returned more than one variable"
        )
        self.assertEqual(
            2,
            len(region_annotations[0]),
            "The number of explanatory features was not 2!"
        )
        outer, inner = region_annotations[0]

        outer_region, inner_region = outer.region, inner.region
        self.assertEqual(
            1,
            len(inner_region.polygon.geoms),
            "Inner region should be comprised of a single polygon!"
        )
        self.assertEqual(
            1,
            len(outer_region.polygon.geoms),
            "Outer region should be comprised of a single polygon!"
        )
        self.assertEqual(len(inner_region.polygon.geoms[0].interiors), 0)
        self.assertEqual(len(outer_region.polygon.geoms[0].interiors), 1)

    def test_construct_region_with_multiple_holes(self):
        np.random.seed(0)

        x = np.random.uniform(-2, 2, size=(500, 2))

        features = pd.DataFrame()
        hole1 = np.linalg.norm(x - [1, 1], axis=1) < 0.5
        hole2 = np.linalg.norm(x - [-1, 1], axis=1) < 0.5
        hole3 = np.linalg.norm(x - [1, -1], axis=1) < 0.5
        hole4 = np.linalg.norm(x - [-1, -1], axis=1) < 0.5
        features["holes"] = hole1 | hole2 | hole3 | hole4
        features["holes"] = features["holes"]

        # The function returns the base variables, of which there should only be one
        region_annotations = vera.an.generate_region_annotations(
            features, embedding=x, scale_factor=0.5, sample_size=None,
        )
        self.assertEqual(
            1,
            len(region_annotations),
            "`an.generate_explanatory_features` returned more than one variable"
        )
        self.assertEqual(
            2,
            len(region_annotations[0]),
            "The number of explanatory features was not 2!"
        )
        outer, inner = region_annotations[0]

        outer_region, inner_region = outer.region, inner.region
        self.assertEqual(
            4,
            len(inner_region.polygon.geoms),
            "Inner region should be comprised of four polygons!"
        )
        self.assertEqual(
            1,
            len(outer_region.polygon.geoms),
            "Outer region should be comprised of a single polygon!"
        )
        self.assertEqual(0, len(inner_region.polygon.geoms[0].interiors))
        self.assertEqual(4, len(outer_region.polygon.geoms[0].interiors))
