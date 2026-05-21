# src/recommendation/recommender.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent.parent))

import json

# ── Paths ────────────────────────────────────────────────────
RECOMMENDATION_DIR = Path(__file__).resolve().parent

DISEASE_INFO_PATH    = RECOMMENDATION_DIR / \
                       "disease_info.json"
TREATMENT_DATA_PATH  = RECOMMENDATION_DIR / \
                       "treatment_data.json"
FARMING_TIPS_PATH    = RECOMMENDATION_DIR / \
                       "farming_tips.json"

# ── Valid Classes ────────────────────────────────────────────
VALID_CLASSES = [
    "healthy",
    "leaf_rust",
    "stripe_rust",
    "powdery_mildew"
]


# ── Load JSON Files ──────────────────────────────────────────
def load_json(file_path):
    """
    Loads a JSON file and returns its contents.
    Raises clear error if file not found.

    file_path : Path to JSON file
    Output    : dict
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(
            f"Data file not found: {file_path}\n"
            f"Make sure all JSON files exist in "
            f"src/recommendation/"
        )
    with open(str(file_path), "r",
              encoding="utf-8") as f:
        return json.load(f)


def load_all_data():
    """
    Loads all three JSON files at once.
    Returns tuple (disease_info,
                   treatment_data,
                   farming_tips)
    """
    disease_info   = load_json(DISEASE_INFO_PATH)
    treatment_data = load_json(TREATMENT_DATA_PATH)
    farming_tips   = load_json(FARMING_TIPS_PATH)
    return disease_info, treatment_data, farming_tips


# ── Get Disease Info ─────────────────────────────────────────
def get_disease_info(disease_class):
    """
    Returns disease information for a given class.

    disease_class : string — one of VALID_CLASSES
    Output        : dict from disease_info.json
    """
    disease_info = load_json(DISEASE_INFO_PATH)

    if disease_class not in VALID_CLASSES:
        raise ValueError(
            f"Unknown disease class: {disease_class}. "
            f"Valid classes: {VALID_CLASSES}"
        )
    return disease_info[disease_class]


# ── Get Treatment ────────────────────────────────────────────
def get_treatment(disease_class):
    """
    Returns treatment data for a given class.

    disease_class : string — one of VALID_CLASSES
    Output        : dict from treatment_data.json
    """
    treatment_data = load_json(TREATMENT_DATA_PATH)

    if disease_class not in VALID_CLASSES:
        raise ValueError(
            f"Unknown disease class: {disease_class}."
        )
    return treatment_data[disease_class]


# ── Get Farming Tips ─────────────────────────────────────────
def get_farming_tips(disease_class):
    """
    Returns fertilizer and farming tips
    for a given disease class.

    disease_class : string — one of VALID_CLASSES
    Output        : dict with relevant tips
    """
    farming_tips = load_json(FARMING_TIPS_PATH)

    fertilizer = farming_tips[
        "fertilizer_recommendations"
    ]["by_disease"][disease_class]

    general    = farming_tips["general_tips"]
    calendar   = farming_tips["seasonal_calendar"]
    varieties  = farming_tips["variety_recommendations"]

    return {
        "fertilizer" : fertilizer,
        "general"    : general,
        "calendar"   : calendar,
        "varieties"  : varieties
    }


# ── Get Complete Recommendation ──────────────────────────────
def get_recommendation(disease_class):
    """
    Main function — returns COMPLETE recommendation
    for a predicted disease class.

    Combines disease_info + treatment + farming_tips
    into one structured dict ready for the frontend.

    disease_class : string — one of VALID_CLASSES
    Output        : dict with all recommendation data
    """
    if disease_class not in VALID_CLASSES:
        return {
            "status"  : "error",
            "message" : f"Unknown disease: {disease_class}"
        }

    try:
        # load all data
        disease_info, treatment_data, farming_tips = \
            load_all_data()

        info      = disease_info[disease_class]
        treatment = treatment_data[disease_class]
        tips      = get_farming_tips(disease_class)

        # build complete recommendation
        recommendation = {
            "status"       : "success",
            "disease_class": disease_class,

            # disease information
            "disease_info" : {
                "display_name"   : info["display_name"],
                "description"    : info["description"],
                "symptoms"       : info["symptoms"],
                "causes"         : info["causes"],
                "severity"       : info["severity"],
                "severity_label" : info["severity_label"],
                "affected_parts" : info["affected_parts"],
                "season_risk"    : info["season_risk"],
                "economic_impact": info["economic_impact"]
            },

            # treatment
            "treatment"    : {
                "immediate_actions"    :
                    treatment["immediate_actions"],
                "chemical_treatments"  :
                    treatment["chemical_treatments"],
                "biological_treatments":
                    treatment["biological_treatments"],
                "preventive_measures"  :
                    treatment["preventive_measures"],
                "application_timing"   :
                    treatment["application_timing"],
                "safety_precautions"   :
                    treatment["safety_precautions"]
            },

            # fertilizer
            "fertilizer"   : {
                "nitrogen"       :
                    tips["fertilizer"]["nitrogen"],
                "phosphorus"     :
                    tips["fertilizer"]["phosphorus"],
                "potassium"      :
                    tips["fertilizer"]["potassium"],
                "micronutrients" :
                    tips["fertilizer"]["micronutrients"],
                "special_notes"  :
                    tips["fertilizer"]["special_notes"]
            },

            # general farming
            "farming"      : {
                "irrigation" :
                    tips["general"]["irrigation"],
                "sowing"     :
                    tips["general"]["sowing"],
                "harvesting" :
                    tips["general"]["harvesting"],
                "varieties"  :
                    tips["varieties"]["rust_resistant"]
            }
        }

        return recommendation

    except Exception as e:
        return {
            "status"  : "error",
            "message" : f"Recommendation failed: {str(e)}"
        }


# ── Format Recommendation For Terminal ───────────────────────
def format_recommendation(rec):
    """
    Formats complete recommendation for
    clean terminal display and testing.

    rec    : dict from get_recommendation()
    Output : formatted string
    """
    if rec["status"] == "error":
        return f"❌ Error: {rec['message']}"

    info      = rec["disease_info"]
    treatment = rec["treatment"]
    fertilizer = rec["fertilizer"]

    lines = [
        "=" * 55,
        f"  RECOMMENDATION: "
        f"{info['display_name'].upper()}",
        "=" * 55,
        "",
        "📋 DISEASE INFORMATION",
        "-" * 55,
        f"  Description  : {info['description']}",
        f"  Severity     : {info['severity_label']}",
        f"  Season Risk  : {info['season_risk']}",
        f"  Economic     : {info['economic_impact']}",
        "",
        "🔍 SYMPTOMS",
        "-" * 55,
    ]

    for s in info["symptoms"]:
        lines.append(f"  • {s}")

    lines += [
        "",
        "⚡ IMMEDIATE ACTIONS",
        "-" * 55,
    ]
    for a in treatment["immediate_actions"]:
        lines.append(f"  • {a}")

    lines += [
        "",
        "💊 CHEMICAL TREATMENTS",
        "-" * 55,
    ]
    for t in treatment["chemical_treatments"]:
        lines.append(f"  • {t['name']}")
        lines.append(f"    Dose    : {t['dose']}")
        lines.append(f"    Method  : {t['method']}")
        lines.append(f"    Brands  : "
                     f"{', '.join(t['brand_names'])}")

    lines += [
        "",
        "🌱 PREVENTIVE MEASURES",
        "-" * 55,
    ]
    for p in treatment["preventive_measures"]:
        lines.append(f"  • {p}")

    lines += [
        "",
        "🌾 FERTILIZER ADVICE",
        "-" * 55,
        f"  Nitrogen   : "
        f"{fertilizer['nitrogen']['total_dose']}",
        f"  Phosphorus : "
        f"{fertilizer['phosphorus']['total_dose']}",
        f"  Potassium  : "
        f"{fertilizer['potassium']['total_dose']}",
        f"  Note       : "
        f"{fertilizer['special_notes']}",
        "",
        "=" * 55
    ]

    return "\n".join(lines)


# ── Quick Test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing recommender.py...\n")

    for disease in VALID_CLASSES:
        print(f"Testing: {disease}")
        rec = get_recommendation(disease)
        if rec["status"] == "success":
            print(f"  ✅ Recommendation generated "
                  f"for {disease}")
        else:
            print(f"  ❌ Error: {rec['message']}")

    print("\n" + "=" * 55)
    print("Full recommendation for stripe_rust:")
    print("=" * 55)
    rec = get_recommendation("stripe_rust")
    print(format_recommendation(rec))