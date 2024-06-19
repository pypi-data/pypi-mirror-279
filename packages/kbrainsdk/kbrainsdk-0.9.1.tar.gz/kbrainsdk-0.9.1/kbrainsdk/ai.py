from kbrainsdk.validation.ai import validate_ai_decide, validate_ai_categorize, validate_ai_tag_document
from kbrainsdk.apibase import APIBase

class AI(APIBase):

    def decide(self, query, choices, examples, **kwargs):
        
        payload = {
            "query": query,
            "choices": choices,
            "examples": examples,
            **kwargs
        }

        validate_ai_decide(payload)

        path = f"/ai/decide/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def categorize(self, query, **kwargs):
        
        payload = {
            "query": query,
            **kwargs
        }

        validate_ai_categorize(payload)

        path = f"/ai/categorize/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def tag_document(self, content, **kwargs):
        
        payload = {
            "content": content,
            **kwargs
        }

        validate_ai_tag_document(payload)

        path = f"/ai/tag_document/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response