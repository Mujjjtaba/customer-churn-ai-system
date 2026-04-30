def generate_recommendation(probability):
    if probability >= 75:
        return "Critical churn risk. Immediate retention offer, dedicated customer support, and contract discount recommended."
    elif probability >= 50:
        return "Moderate churn risk. Personalized loyalty rewards and service quality follow-up recommended."
    elif probability >= 30:
        return "Mild churn tendency. Customer engagement campaign recommended."
    else:
        return "Low churn risk. Maintain normal relationship management."