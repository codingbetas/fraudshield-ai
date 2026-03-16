metrics = {
    "total_predictions": 0,
    "fraud_predictions": 0
}

def update_metrics(is_fraud):

    metrics["total_predictions"] += 1

    if is_fraud:
        metrics["fraud_predictions"] += 1


def get_metrics():
    return metrics