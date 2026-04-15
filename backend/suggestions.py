# ============================================================
#  RETINAL DR DETECTION — AI SUGGESTIONS
#  Built-in care suggestions + Gemini API placeholder
# ============================================================


# ==============================================================
# BUILT-IN CARE SUGGESTIONS (per DR grade)
# ==============================================================

CARE_SUGGESTIONS = {
    0: {
        "title": "Healthy Retina — Preventive Care",
        "summary": "Great news! No signs of diabetic retinopathy were detected. Continue maintaining your eye health with these recommendations.",
        "recommendations": [
            {
                "category": "Regular Screening",
                "icon": "🔍",
                "items": [
                    "Schedule annual comprehensive dilated eye exams",
                    "Monitor vision changes and report them promptly",
                    "Keep a record of your eye examination history"
                ]
            },
            {
                "category": "Blood Sugar Management",
                "icon": "🩸",
                "items": [
                    "Maintain HbA1c levels below 7% (or as recommended by your doctor)",
                    "Monitor blood glucose levels regularly",
                    "Follow your prescribed diabetes management plan"
                ]
            },
            {
                "category": "Lifestyle & Diet",
                "icon": "🥗",
                "items": [
                    "Eat a balanced diet rich in leafy greens, omega-3 fatty acids, and antioxidants",
                    "Include foods high in vitamins A, C, and E (carrots, citrus, nuts)",
                    "Limit refined carbohydrates and processed sugars",
                    "Stay hydrated — aim for 8 glasses of water daily"
                ]
            },
            {
                "category": "Physical Activity",
                "icon": "🏃",
                "items": [
                    "Engage in at least 150 minutes of moderate aerobic activity per week",
                    "Include resistance training 2-3 times per week",
                    "Avoid exercises that significantly raise eye pressure (heavy lifting with Valsalva)"
                ]
            },
            {
                "category": "General Health",
                "icon": "💊",
                "items": [
                    "Maintain blood pressure below 130/80 mmHg",
                    "Monitor and manage cholesterol levels",
                    "Avoid smoking — it accelerates retinal damage",
                    "Wear UV-protective sunglasses outdoors"
                ]
            }
        ]
    },
    1: {
        "title": "Mild DR — Early Intervention",
        "summary": "Mild non-proliferative diabetic retinopathy has been detected. Small microaneurysms are present. Early intervention can prevent progression.",
        "recommendations": [
            {
                "category": "Follow-up Schedule",
                "icon": "📅",
                "items": [
                    "Schedule eye exams every 6-9 months",
                    "Request OCT (Optical Coherence Tomography) scans to monitor retinal thickness",
                    "Document any changes in vision (blurriness, floaters, dark spots)"
                ]
            },
            {
                "category": "Strict Blood Sugar Control",
                "icon": "🩸",
                "items": [
                    "Target HbA1c below 7% — even small improvements reduce progression risk by 25%",
                    "Monitor fasting blood glucose daily",
                    "Consider continuous glucose monitoring (CGM) if available",
                    "Work with your endocrinologist to optimize medication"
                ]
            },
            {
                "category": "Blood Pressure & Cholesterol",
                "icon": "❤️",
                "items": [
                    "Maintain blood pressure below 130/80 mmHg",
                    "Take prescribed antihypertensive medications consistently",
                    "Monitor LDL cholesterol — target below 100 mg/dL",
                    "Consider statin therapy if recommended"
                ]
            },
            {
                "category": "Diet Modifications",
                "icon": "🥗",
                "items": [
                    "Follow a Mediterranean or DASH diet",
                    "Increase intake of lutein and zeaxanthin (spinach, kale, eggs)",
                    "Reduce sodium intake to less than 2,300 mg/day",
                    "Limit alcohol consumption"
                ]
            },
            {
                "category": "Lifestyle Changes",
                "icon": "🧘",
                "items": [
                    "Quit smoking immediately — smoking doubles DR progression risk",
                    "Manage stress through meditation, yoga, or relaxation techniques",
                    "Ensure 7-8 hours of quality sleep per night",
                    "Protect eyes from bright light and UV exposure"
                ]
            }
        ]
    },
    2: {
        "title": "Moderate DR — Specialist Care Needed",
        "summary": "Moderate non-proliferative diabetic retinopathy detected with more widespread vascular changes. Professional ophthalmological care is important at this stage.",
        "recommendations": [
            {
                "category": "Urgent Medical Actions",
                "icon": "🏥",
                "items": [
                    "Schedule an appointment with a retinal specialist within 2-4 weeks",
                    "Get a comprehensive fluorescein angiography to map blood vessel damage",
                    "Regular OCT imaging every 3-4 months",
                    "Discuss treatment options with your ophthalmologist"
                ]
            },
            {
                "category": "Aggressive Blood Sugar Control",
                "icon": "🩸",
                "items": [
                    "Target HbA1c below 6.5% if possible without hypoglycemia",
                    "Consider insulin therapy adjustments",
                    "Use continuous glucose monitoring for tighter control",
                    "Coordinate care between your endocrinologist and ophthalmologist"
                ]
            },
            {
                "category": "Potential Treatments",
                "icon": "💉",
                "items": [
                    "Anti-VEGF injections may be recommended if macular edema is present",
                    "Laser photocoagulation might be considered for specific areas",
                    "Intravitreal corticosteroid implants in select cases",
                    "Discuss risks and benefits of each treatment option"
                ]
            },
            {
                "category": "Monitoring Symptoms",
                "icon": "👁️",
                "items": [
                    "Watch for sudden vision changes — seek immediate care if they occur",
                    "Monitor for increased floaters or flashes of light",
                    "Test each eye separately daily using an Amsler grid",
                    "Report any difficulty with night vision or color perception"
                ]
            },
            {
                "category": "Comprehensive Health Management",
                "icon": "💊",
                "items": [
                    "Maintain strict blood pressure control (below 130/80 mmHg)",
                    "Optimize lipid levels with medication if needed",
                    "Address any kidney function concerns (DR and nephropathy often coexist)",
                    "Consider aspirin therapy as discussed with your doctor"
                ]
            }
        ]
    },
    3: {
        "title": "Severe DR — Urgent Care Required",
        "summary": "Severe non-proliferative diabetic retinopathy detected with significant vascular damage. Prompt specialist intervention is critical to prevent vision loss.",
        "recommendations": [
            {
                "category": "Immediate Actions",
                "icon": "🚨",
                "items": [
                    "See a retinal specialist within 1-2 weeks — do not delay",
                    "Get urgent fluorescein angiography and OCT imaging",
                    "Discuss panretinal photocoagulation (PRP) laser treatment",
                    "Prepare for possible anti-VEGF injection therapy"
                ]
            },
            {
                "category": "Treatment Options",
                "icon": "💉",
                "items": [
                    "Panretinal photocoagulation (PRP) — reduces risk of severe vision loss by 50%",
                    "Anti-VEGF injections (Avastin, Lucentis, Eylea) to reduce swelling",
                    "Combination therapy may be recommended",
                    "Monthly monitoring during active treatment"
                ]
            },
            {
                "category": "Critical Blood Sugar Management",
                "icon": "🩸",
                "items": [
                    "Intensive insulin therapy or medication adjustment required",
                    "Target HbA1c reduction gradually — sudden drops can temporarily worsen DR",
                    "Monitor blood glucose at least 4 times daily",
                    "Coordinate closely with your diabetes care team"
                ]
            },
            {
                "category": "Vision Preservation",
                "icon": "👁️",
                "items": [
                    "Learn to use the Amsler grid and check daily",
                    "Any sudden vision changes = emergency room visit",
                    "Consider low-vision aids if needed",
                    "Discuss driving safety with your doctor"
                ]
            },
            {
                "category": "Emotional & Support",
                "icon": "🤝",
                "items": [
                    "Connect with diabetic retinopathy support groups",
                    "Consider counseling — diagnosis of severe DR can be emotionally challenging",
                    "Involve family members in your care plan",
                    "Stay informed but avoid unverified online sources"
                ]
            }
        ]
    },
    4: {
        "title": "Proliferative DR — Emergency Attention",
        "summary": "Proliferative diabetic retinopathy detected with abnormal new blood vessel growth. This is the most advanced stage and requires immediate medical intervention to prevent severe vision loss.",
        "recommendations": [
            {
                "category": "Emergency Medical Care",
                "icon": "🚑",
                "items": [
                    "Seek immediate consultation with a vitreoretinal surgeon",
                    "Emergency treatment may be needed within days",
                    "Do NOT delay — risk of retinal detachment and severe vision loss is high",
                    "Bring all previous medical records and imaging to your appointment"
                ]
            },
            {
                "category": "Advanced Treatments",
                "icon": "🔬",
                "items": [
                    "Panretinal photocoagulation (PRP) laser surgery — primary treatment",
                    "Anti-VEGF injections to control neovascularization",
                    "Vitrectomy surgery if vitreous hemorrhage or retinal detachment occurs",
                    "Combination of laser + injections is often most effective"
                ]
            },
            {
                "category": "Post-Treatment Care",
                "icon": "🏥",
                "items": [
                    "Follow all post-operative instructions strictly",
                    "Attend all follow-up appointments — typically weekly initially",
                    "Report any sudden vision loss, severe pain, or increased floaters immediately",
                    "Expect multiple treatment sessions over weeks to months"
                ]
            },
            {
                "category": "Systemic Health Management",
                "icon": "💊",
                "items": [
                    "Intensive multi-disciplinary care (endocrinologist, nephrologist, cardiologist)",
                    "Strict blood sugar, blood pressure, and lipid control",
                    "Screen for other diabetic complications (neuropathy, nephropathy)",
                    "Medication review and optimization"
                ]
            },
            {
                "category": "Long-term Support",
                "icon": "🤝",
                "items": [
                    "Register with low-vision rehabilitation services if needed",
                    "Explore assistive technologies for daily tasks",
                    "Join diabetic retinopathy support communities",
                    "Mental health support — anxiety and depression screening recommended",
                    "Plan for ongoing monitoring even after successful treatment"
                ]
            }
        ]
    }
}


def get_suggestions(grade: int) -> dict:
    """
    Get built-in care suggestions for a given DR grade.

    Args:
        grade: int (0-4) — predicted DR grade

    Returns:
        dict with title, summary, and recommendations
    """
    if grade not in CARE_SUGGESTIONS:
        return {
            "title": "Unknown Grade",
            "summary": "Unable to provide suggestions for this grade.",
            "recommendations": []
        }
    return CARE_SUGGESTIONS[grade]
