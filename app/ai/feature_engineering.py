def create_features(amount, oldbalanceOrg, newbalanceOrig):

    balance_diff = oldbalanceOrg - newbalanceOrig

    ratio = 0
    if oldbalanceOrg > 0:
        ratio = amount / oldbalanceOrg

    return [
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        balance_diff,
        ratio
    ]