"""
Single source of truth for feature construction.

ALL models (Random Forest, Isolation Forest) use this function.
Training and inference MUST call this with the same inputs.

FEATURE_NAMES is set from select_features.py output.
"""

# UPDATE THIS with the output from select_features.py
FEATURE_NAMES = ['V14', 'V10', 'V12', 'V4', 'V17', 'V3', 'V11', 'V16']  # example only — replace with your actual top 8


def build_features(features_dict):
    """
    Build the canonical feature vector in FEATURE_NAMES order.

    Input:
        features_dict: dict mapping feature name → value
                       (e.g., {"V14": -0.5, "Amount": 100.0, ...})

    Returns:
        list of floats, in FEATURE_NAMES order.
    """
    missing = [name for name in FEATURE_NAMES if name not in features_dict]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    return [float(features_dict[name]) for name in FEATURE_NAMES]