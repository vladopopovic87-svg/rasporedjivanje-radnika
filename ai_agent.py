# AI Agent for parameter extraction using Groq API

from groq import Groq
import streamlit as st
import json
import os
from typing import Dict, Any

# Initialize Groq client
def init_groq(api_key: str = None):
    """Initialize Groq API with API key."""
    if api_key:
        return Groq(api_key=api_key)
    elif os.getenv("GROQ_API_KEY"):
        return Groq(api_key=os.getenv("GROQ_API_KEY"))
    else:
        raise ValueError("GROQ_API_KEY not found. Please provide an API key.")


def extract_parameters_from_description(description: str, client: Groq) -> Dict[str, Any]:
    """
    Use Groq to extract scheduling parameters from a user description.
    
    Args:
        description: User's problem description in natural language
        client: Groq client instance
        
    Returns:
        Dictionary with extracted parameters
    """
    try:
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

Budi precizna u analizi i vrati samo JSON bez dodatnog teksta."""

        message = client.messages.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        
        response_text = message.content[0].text.strip()
        
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


def get_ai_suggestions(description: str, client: Groq) -> str:
    """
    Get general AI suggestions for the problem.
    
    Args:
        description: User's problem description
        client: Groq client instance
        
    Returns:
        Formatted suggestions string
    """
    try:
        prompt = f"""Kao ekspert za raspoređivanje radnika i optimizaciju, daj kratke i praktične preporuke za sledeći problem:

{description}

Daj 3-4 konkretne preporuke na srpskom jeziku."""

        message = client.messages.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=512
        )
        
        return message.content[0].text
        
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
