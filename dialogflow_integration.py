# dialogflow_integration.py
import logging
from google.cloud import dialogflow

logger = logging.getLogger(__name__)

def detect_intent(text, session_id, project_id, language_code='es'):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        
        return response.query_result.fulfillment_text
        
    except Exception as e:
        logger.error(f"Error con DialogFlow: {e}")
        return None  # o return "Lo siento, no puedo responder ahora"
