"""
Tests for the feature engineering module.

The canonical 8-feature vector must match FEATURE_NAMES.
"""

from app.ai.feature_engineering import FEATURE_NAMES, build_features


def test_feature_names_length():
    """Random Forest selected 8 features."""
    assert len(FEATURE_NAMES) == 8


def test_build_features_returns_correct_length():
    """build_features returns one float per feature in FEATURE_NAMES."""
    features_dict = {
        "V14": -0.5,
        "V10": -0.3,
        "V12": -0.4,
        "V4": 0.8,
        "V17": -0.2,
        "V3": 0.5,
        "V11": 0.6,
        "V16": -0.4,
    }

    result = build_features(features_dict)
    assert len(result) == len(FEATURE_NAMES)
    assert all(isinstance(v, float) for v in result)


def test_build_features_preserves_order():
    """Features are returned in the same order as FEATURE_NAMES."""
    features_dict = {
        "V14": 1.0,
        "V10": 2.0,
        "V12": 3.0,
        "V4": 4.0,
        "V17": 5.0,
        "V3": 6.0,
        "V11": 7.0,
        "V16": 8.0,
    }

    result = build_features(features_dict)

    expected = [float(features_dict[name]) for name in FEATURE_NAMES]
    assert result == expected