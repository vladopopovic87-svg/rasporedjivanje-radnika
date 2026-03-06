# AI Agent for parameter extraction using Google Gemini API

import google.generativeai as genai
import streamlit as st
import json
import os
from typing import Dict, Any

# Configure Gemini API
def init_gemini(api_key: str = None):
    """Initialize Gemini API with API key."""
    if api_key:
        genai.configure(api_key=api_key)
    elif os.getenv("GEMINI_API_KEY"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    else:
        raise ValueError("GEMINI_API_KEY not found. Please provide an API key.")


def extract_parameters_from_description(description: str) -> Dict[str, Any]:
    """
    Use Gemini to extract scheduling parameters from a user description.
    
    Args:
        description: User's problem description in natural language
        
    Returns:
        Dictionary with extracted parameters
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Kao ekspert za raspoređivanje radnika, analiziraj sledeći opis problema i ekstraktuj sve relevantne parametre za optimizaciju.

Opis problema:
{description}

Molim te da analiziraš i vrati JSON sa sledećim poljima (koristi brojeve gde je moguće):
{{
    "num_profiles": <broj različitih profila radnika>,
    "profiles": [<lista profila sa opisima>],
    "num_activities": <broj aktivnosti>,
    "activities": [<lista aktivnosti sa opisima>],
    "short_penalty": <vrednost penala od 0-1 za kratke dodeljenosti (0.0-1.0)>,
    "max_workers_per_interval": <maksimalan broj radnika po intervalu>,
    "additional_notes": "<dodatne napomene ili zahtevi>"
}}

Budi presiznana analizi i vrati samo JSON bez dodatnog teksta."""

        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            parameters = json.loads(json_str)
            return parameters
        else:
            return {"error": "Could not parse response"}
            
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}


def get_ai_suggestions(description: str) -> str:
    """
    Get general AI suggestions for the problem.
    
    Args:
        description: User's problem description
        
    Returns:
        Formatted suggestions string
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Kao ekspert za raspoređivanje radnika i optimizaciju, daj kratke i praktične preporuke za sledeći problem:

{description}

Daj 3-4 konkretne preporuke na srpskom jeziku."""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Greška pri komunikaciji sa AI: {str(e)}"


def validate_and_apply_parameters(params: Dict[str, Any]) -> bool:
    """
    Validate extracted parameters and apply them to session state.
    
    Args:
        params: Dictionary of extracted parameters
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if "error" in params:
            st.error(f"AI Greška: {params['error']}")
            return False
            
        # Validation
        if "num_profiles" not in params or params["num_profiles"] < 1:
            st.error("Broj profila mora biti barem 1")
            return False
            
        if "num_activities" not in params or params["num_activities"] < 1:
            st.error("Broj aktivnosti mora biti barem 1")
            return False
            
        if "short_penalty" in params:
            penalty = float(params["short_penalty"])
            if penalty < 0 or penalty > 1:
                st.warning(f"Penala vrednost je van opsega. Koristi se 0.0")
                params["short_penalty"] = 0.0
        else:
            params["short_penalty"] = 0.0
            
        # Store in session state
        st.session_state.ai_extracted_params = params
        return True
        
    except Exception as e:
        st.error(f"Greška pri validaciji parametara: {str(e)}")
        return False
