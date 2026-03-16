def calculate_risk(probability):

    if probability > 0.8:
        return "HIGH"

    if probability > 0.5:
        return "MEDIUM"

    return "LOW"