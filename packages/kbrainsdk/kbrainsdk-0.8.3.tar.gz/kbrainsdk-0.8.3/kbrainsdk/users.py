from kbrainsdk.validation.users import validate_user_entra_groups
from kbrainsdk.apibase import APIBase

class User(APIBase):
    
    def user_entra_groups(self, email, token, client_id, oauth_secret, tenant_id):    
            payload = {
                "email": email,
                "token": token,
                "client_id": client_id,
                "oauth_secret": oauth_secret,
                "tenant_id": tenant_id
            }
    
            validate_user_entra_groups(payload)
    
            path = f"/user/entra/groups/v1"
            response = self.apiobject.call_endpoint(path, payload, "post")
            return response

            