import os
import re
import json
from groq import Groq
from app.core.logger import logger
from app.core.config import settings

LANGUAGE_NAMES = {
    "en": "English",
    "en-IN": "English",
    "hi": "Hindi (हिन्दी)",
    "hi-IN": "Hindi (हिन्दी)",
    "ta": "Tamil (தமிழ்)",
    "ta-IN": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "te-IN": "Telugu (తెలుగు)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "kn-IN": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "ml-IN": "Malayalam (മലയാളം)",
}

PREFERRED_GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]


class AgriculturalNLPEngine:
    def __init__(self):
        self.groq_api_key = settings.GROQ_API_KEY
        self.active_groq_model = None
        self.available_groq_models = []

        if self.groq_api_key:
            logger.info(
                "Groq API key detected. Initializing Groq cloud client for high-speed NLP."
            )
            self.groq_client = Groq(api_key=self.groq_api_key)
            self._select_working_groq_model()
        else:
            self.groq_client = None
            logger.warning("No Groq API key found. Using built-in agricultural knowledge engine.")

        self.candidate_labels = [
            "CROP_ADVISORY",
            "PEST_CONTROL",
            "DISEASE_MANAGEMENT",
            "FERTILIZER_ADVICE",
            "IRRIGATION_ADVICE",
            "MARKET_PRICES",
            "WEATHER_INFO",
            "SCHEME_LOOKUP",
        ]
        self.classifier = None
        self.ner_qa = None

    def _select_working_groq_model(self) -> str:
        if self.active_groq_model and self.available_groq_models:
            return self.active_groq_model
        if not self.groq_client:
            return "openai/gpt-oss-120b"
        try:
            models_resp = self.groq_client.models.list()
            available_ids = [
                m.id
                for m in getattr(models_resp, "data", [])
                if not any(
                    skip in m.id.lower()
                    for skip in (
                        "whisper",
                        "tts",
                        "guard",
                        "prompt-guard",
                        "orpheus",
                        "allam",
                        "playai",
                        "embed",
                    )
                )
            ]
            logger.info(f"Available Groq chat models: {available_ids}")
            ordered = []
            for candidate in PREFERRED_GROQ_MODELS:
                if candidate in available_ids:
                    ordered.append(candidate)
            for m_id in available_ids:
                if m_id not in ordered:
                    ordered.append(m_id)
            if ordered:
                self.available_groq_models = ordered
                self.active_groq_model = ordered[0]
                logger.info(f"Selected active Groq model: {self.active_groq_model}")
                return self.active_groq_model
        except Exception as e:
            logger.warning(f"Could not list Groq models dynamically: {e}")

        self.available_groq_models = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]
        self.active_groq_model = self.available_groq_models[0]
        return self.active_groq_model

    def _parse_structured_output(self, raw_content: str, raw_query: str) -> dict:
        """
        Resilient parser that supports both labeled sections and JSON responses,
        ensuring multiline answers in Indian scripts never fail to parse.
        """
        text = raw_content.strip()
        if "<think>" in text and "</think>" in text:
            text = text.split("</think>")[-1].strip()

        # 1. Check if labeled sections are present
        if "ENGLISH_RESPONSE:" in text or "TRANSLATED_RESPONSE:" in text:
            intent_match = re.search(r"INTENT:\s*(.+)", text)
            crop_match = re.search(r"CROP:\s*(.+)", text)
            issue_match = re.search(r"ISSUE:\s*(.+)", text)
            query_match = re.search(r"CANONICAL_QUERY:\s*(.+)", text)

            intent = intent_match.group(1).strip() if intent_match else "CROP_ADVISORY"
            crop = crop_match.group(1).strip() if crop_match else "general"
            issue = issue_match.group(1).strip() if issue_match else "advisory"
            canonical_query = query_match.group(1).strip() if query_match else raw_query

            eng_resp = ""
            trans_resp = ""

            if "ENGLISH_RESPONSE:" in text and "TRANSLATED_RESPONSE:" in text:
                parts = text.split("ENGLISH_RESPONSE:", 1)[1]
                eng_part, trans_part = parts.split("TRANSLATED_RESPONSE:", 1)
                eng_resp = eng_part.strip()
                trans_resp = trans_part.strip()
            elif "TRANSLATED_RESPONSE:" in text:
                trans_resp = text.split("TRANSLATED_RESPONSE:", 1)[1].strip()
                eng_resp = trans_resp
            elif "ENGLISH_RESPONSE:" in text:
                eng_resp = text.split("ENGLISH_RESPONSE:", 1)[1].strip()
                trans_resp = eng_resp

            if eng_resp or trans_resp:
                return {
                    "canonical_query": canonical_query,
                    "intent": intent.upper().replace(" ", "_"),
                    "entities": {"crop": crop, "topic": issue},
                    "canonical_response": eng_resp or trans_resp,
                    "translated_response": trans_resp or eng_resp,
                }

        # 2. Try JSON parsing (with strict=False to tolerate newlines inside strings)
        cleaned = text
        if "```" in cleaned:
            for block in cleaned.split("```"):
                b = block.replace("json", "", 1).strip()
                if b.startswith("{") and b.endswith("}"):
                    cleaned = b
                    break
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        if start_idx != -1 and end_idx != -1:
            json_candidate = cleaned[start_idx : end_idx + 1]
            try:
                parsed = json.loads(json_candidate, strict=False)
                if parsed.get("canonical_response") or parsed.get("translated_response"):
                    return {
                        "canonical_query": parsed.get("canonical_query") or raw_query,
                        "intent": parsed.get("intent") or "CROP_ADVISORY",
                        "entities": parsed.get("entities") if isinstance(parsed.get("entities"), dict) else {},
                        "canonical_response": parsed.get("canonical_response") or parsed.get("translated_response"),
                        "translated_response": parsed.get("translated_response") or parsed.get("canonical_response"),
                    }
            except Exception:
                # Regex key fallback for partially malformed JSON
                c_match = re.search(r'"canonical_response"\s*:\s*"((?:[^"\\]|\\.)*)"', json_candidate, re.DOTALL)
                t_match = re.search(r'"translated_response"\s*:\s*"((?:[^"\\]|\\.)*)"', json_candidate, re.DOTALL)
                i_match = re.search(r'"intent"\s*:\s*"([^"]+)"', json_candidate)
                if c_match or t_match:
                    c_val = c_match.group(1).replace("\\n", "\n") if c_match else ""
                    t_val = t_match.group(1).replace("\\n", "\n") if t_match else c_val
                    return {
                        "canonical_query": raw_query,
                        "intent": i_match.group(1) if i_match else "CROP_ADVISORY",
                        "entities": {},
                        "canonical_response": c_val or t_val,
                        "translated_response": t_val or c_val,
                    }

        # 3. Plain-text fallback: never discard a valid non-empty LLM response
        if len(text) > 15:
            return {
                "canonical_query": raw_query,
                "intent": "CROP_ADVISORY",
                "entities": {},
                "canonical_response": text,
                "translated_response": text,
            }
        return None

    def generate_full_advisory(
        self, raw_query: str, target_lang_code: str = "en-IN", extra_context: str = ""
    ) -> dict:
        """
        Uses Groq LLM to understand the farmer's query in any language, extract intent & entities,
        generate a detailed, accurate agricultural advisory answer in English, and translate it
        into the target language (Hindi, Tamil, Telugu, Kannada, Malayalam, or English).
        """
        if not target_lang_code or target_lang_code == "auto":
            target_lang_code = "en-IN"
        if len(target_lang_code) == 2:
            target_lang_code = f"{target_lang_code}-IN"

        target_lang_name = LANGUAGE_NAMES.get(
            target_lang_code,
            LANGUAGE_NAMES.get(target_lang_code.split("-")[0], "English"),
        )
        is_english = target_lang_code.lower().startswith("en")

        if self.groq_client:
            self._select_working_groq_model()
            system_prompt = (
                "You are AgriAI, a senior Indian Agricultural Extension Scientist & Agronomist.\n"
                "Directly answer the farmer's exact question with clear, practical, actionable farming advice "
                "(including specific symptoms, organic remedies, recommended treatment dosages, fertilizer schedules, "
                "irrigation tips, or scheme details as relevant).\n\n"
                "Format your response using these EXACT section headers (do NOT wrap in JSON):\n"
                "INTENT: <one of CROP_ADVISORY, PEST_CONTROL, DISEASE_MANAGEMENT, FERTILIZER_ADVICE, IRRIGATION_ADVICE, WEATHER_INFO, MARKET_PRICES, SCHEME_LOOKUP>\n"
                "CROP: <crop name or General Farming>\n"
                "ISSUE: <short topic summary>\n"
                "CANONICAL_QUERY: <1-sentence English translation of the farmer's question>\n"
                "ENGLISH_RESPONSE:\n"
                "<Write a comprehensive, clear, actionable 4-6 point agricultural advisory answer in English>\n"
                "TRANSLATED_RESPONSE:\n"
                f"<Write the complete agricultural advisory answer naturally and accurately in {target_lang_name} ({target_lang_code})>"
            )

            user_msg = (
                f"Farmer's Question: {raw_query}\n"
                f"Required Output Language for TRANSLATED_RESPONSE: {target_lang_name} ({target_lang_code})"
            )
            if extra_context:
                user_msg += f"\nAdditional Context: {extra_context}"

            models_to_try = list(self.available_groq_models) if self.available_groq_models else PREFERRED_GROQ_MODELS[:3]
            for m_id in models_to_try[:3]:
                try:
                    logger.info(
                        f"Generating full AI advisory via Groq model '{m_id}' for language '{target_lang_code}'..."
                    )
                    completion = self.groq_client.chat.completions.create(
                        model=m_id,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_msg},
                        ],
                        temperature=0.25,
                        max_tokens=1400,
                    )
                    self.active_groq_model = m_id
                    raw_content = completion.choices[0].message.content or ""
                    parsed = self._parse_structured_output(raw_content, raw_query)
                    if parsed:
                        if is_english:
                            parsed["translated_response"] = parsed["canonical_response"]
                        return parsed
                except Exception as e:
                    logger.warning(f"Groq model '{m_id}' error: {e}")
                    continue

        # Built-in offline expert fallback if cloud API is unreachable
        return self._generate_builtin_expert_advisory(raw_query, target_lang_code)

    def _generate_builtin_expert_advisory(self, raw_query: str, target_lang_code: str) -> dict:
        q_lower = raw_query.lower()
        intent = "CROP_ADVISORY"
        crop = "Crop"
        for c_name in ["tomato", "paddy", "rice", "wheat", "cotton", "onion", "potato", "maize", "chilli", "banana", "sugarcane"]:
            if c_name in q_lower:
                crop = c_name.title()
                break

        if any(k in q_lower for k in ["pest", "insect", "worm", "borer", "aphid", "thrip", "whitefly", "कीड़", "कीट", "பூச்சி", "పురుగు", "ಕೀಟ", "കീട"]):
            intent = "PEST_CONTROL"
            eng = (
                f"Integrated Pest Management (IPM) Advisory for {crop}:\n"
                "1. Field Sanitation: Remove heavily infested leaves/shoots and install 8-10 yellow/blue sticky traps per acre.\n"
                "2. Organic Spray (First Line): Spray Neem Oil (Azadirachtin 1500 ppm) at 3 ml per liter of water, or NSKE 5%, covering the undersides of leaves.\n"
                "3. Biological Control: Apply Beauveria bassiana or Lecanicillium lecanii @ 5 g/liter during evening hours.\n"
                "4. Targeted Control (if above ETL): Spray Imidacloprid 17.8 SL @ 0.5 ml/L (for sucking pests) or Emamectin Benzoate 5 SG @ 0.4 g/L (for borers/caterpillars)."
            )
        elif any(k in q_lower for k in ["fertilizer", "urea", "npk", "dap", "manure", "nutrient", "खाद", "उर्वरक", "உரம்", "ఎరువు", "ಗೊಬ್ಬರ", "വളം"]):
            intent = "FERTILIZER_ADVICE"
            eng = (
                f"Balanced Nutrient & Fertilizer Schedule for {crop}:\n"
                "1. Basal Application: Apply 5-10 tonnes/acre of well-decomposed Farm Yard Manure (FYM) enriched with Trichoderma and Azospirillum.\n"
                "2. NPK Split Dosing: Apply full Phosphorus (DAP/SSP) and Potash (MOP) as basal; split Nitrogen (Urea) into 3 equal doses at basal, vegetative (25-30 DAS), and flowering stages.\n"
                "3. Micronutrient Correction: Spray Zinc Sulphate (0.5%) + Boron (0.2%) during active vegetative growth to prevent deficiency and flower drop.\n"
                "4. Soil Health Tip: Always irrigate lightly before top-dressing Urea and avoid applying before heavy rainfall."
            )
        elif any(k in q_lower for k in ["disease", "blight", "rot", "yellow", "wilt", "fungus", "curl", "रोग", "நோய்", "இலை", "తెగులు", "ರೋಗ", "രോഗം"]):
            intent = "DISEASE_MANAGEMENT"
            eng = (
                f"Disease Diagnosis & Control Guide for {crop}:\n"
                "1. Moisture & Drainage: Immediately drain excess standing water and avoid overhead sprinkler irrigation to reduce humidity.\n"
                "2. Biological Protection: Soil drenching with Trichoderma viride + Pseudomonas fluorescens @ 5 g/liter around the root zone.\n"
                "3. Fungicide Spray: For leaf spot/early blight, spray Mancozeb 75 WP @ 2.5 g/L or Copper Oxychloride @ 3 g/L. For severe blight/rot, apply Azoxystrobin + Tebuconazole @ 1 ml/L.\n"
                "4. Viral Leaf Curl: Control whitefly/thrips vectors immediately using Neem oil (3 ml/L) and remove severely stunted plants."
            )
        elif any(k in q_lower for k in ["scheme", "pm-kisan", "kisan", "insurance", "subsidy", "loan", "योजना", "திட்டம்", "పథకం", "ಯೋಜನೆ", "പദ്ധതി"]):
            intent = "SCHEME_LOOKUP"
            eng = (
                "Key Government Agricultural Schemes for Farmers:\n"
                "1. PM-KISAN: ₹6,000/year direct income support in 3 installments of ₹2,000 each via DBT (pmkisan.gov.in).\n"
                "2. Pradhan Mantri Fasal Bima Yojana (PMFBY): Low-premium crop insurance (1.5% Rabi, 2% Kharif) against natural calamities.\n"
                "3. Kisan Credit Card (KCC): Short-term crop loans up to ₹3 lakh at 4% effective interest rate with prompt repayment.\n"
                "4. Soil Health Card & PMKSY: Free soil testing every 3 years and up to 55-80% subsidy on drip/sprinkler micro-irrigation."
            )
        else:
            eng = (
                f"Expert Agricultural Advisory for your query ({raw_query}):\n"
                "1. Soil & Seed Prep: Test soil pH (ideal 6.0-7.2) and treat seeds with Trichoderma viride (4 g/kg) before sowing.\n"
                "2. Water & Nutrient Management: Maintain optimal root-zone moisture using drip/ridge-furrow irrigation and apply split NPK doses with organic compost.\n"
                "3. Crop Protection: Scout fields twice weekly; use Neem oil (3 ml/L) and yellow sticky traps as preventive protection against pests and fungal blight.\n"
                "4. Local Support: Check daily APMC mandi trends and weather alerts on this dashboard before harvesting or spraying."
            )

        return {
            "canonical_query": raw_query,
            "intent": intent,
            "entities": {"crop": crop},
            "canonical_response": eng,
            "translated_response": eng,
        }

    def process_query(self, canonical_query: str) -> dict:
        """
        Dynamically extracts structural intent and entities from an English query.
        """
        res = self.generate_full_advisory(canonical_query, target_lang_code="en-IN")
        if res:
            return {
                "intent": res.get("intent", "CROP_ADVISORY"),
                "entities": res.get("entities", {}),
                "canonical_response": res.get("canonical_response"),
            }
        return {"intent": "CROP_ADVISORY", "entities": {}}


# Global structural initialization singleton
nlp_engine = AgriculturalNLPEngine()
