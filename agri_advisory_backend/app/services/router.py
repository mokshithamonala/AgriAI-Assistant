from app.services.nlp_engine import nlp_engine

def classify_and_route(user_query: str):
    result = nlp_engine.process_query(user_query)

    intent = result["intent"]

    if intent == "CROP_ADVISORY":
        route = "RAG_PIPELINE"
    elif intent == "MARKET_PRICES":
        route = "MANDI_API"
    elif intent == "WEATHER_INFO":
        route = "WEATHER_API"
    elif intent == "SCHEME_LOOKUP":
        route = "SCHEME_API"
    else:
        route = "UNKNOWN"

    return {
        "intent": intent,
        "route": route,
        "entities": result.get("entities", {})
    }
