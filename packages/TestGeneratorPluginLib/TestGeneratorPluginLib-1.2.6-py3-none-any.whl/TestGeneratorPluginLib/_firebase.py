from urllib.parse import quote

import requests

FIREBASE_API_KEY = "AIzaSyA9z3kwZsj_VDWGnrzpP2G13bLdHS2VTds"


class FirebaseService:
    def __init__(self, email: str = None, password: str = None):
        self._email = email
        self._password = password
        self._id_token = None
        self._user_id = None

    def log_in(self, sign_up=False):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:{'signUp' if sign_up else 'signInWithPassword'}" \
              f"?key={FIREBASE_API_KEY}"
        try:
            if not self._email:
                self._email = input("Email: ")
            if not self._password:
                self._password = input("Password: ")
            if sign_up:
                password_again = input("Password again: ")
                if password_again != self._password:
                    print("Passwords do not match")
                    return False

            resp = requests.post(url, data={
                "email": self._email,
                "password": self._password,
                "returnSecureToken": True
            })
            res = resp.json()
            if resp.ok:
                self._id_token = res["idToken"]
                self._user_id = res["localId"]
                return True
            else:
                print(f"Error: {res.get('error', dict()).get('message')}")

        except requests.ConnectionError:
            print("Connection error")
        return False

    def verify_email(self):
        url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={FIREBASE_API_KEY}"
        data = {"requestType": "VERIFY_EMAIL", "idToken": self._id_token}
        print(data)
        resp = requests.post(url, data=data)
        if not resp.ok:
            raise Exception(resp.text)

    def upload_metadata(self, name: str, metadata: dict | str):
        url = f"https://testgenerator-bf37c-default-rtdb.europe-west1.firebasedatabase.app/plugins/" \
              f"{self._user_id}/{name}.json?auth={self._id_token}"
        resp = requests.patch(url, json=metadata)
        if not resp.ok:
            raise Exception(f"Error: {resp.text}")

    def upload_file(self, path, name=None):
        url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
              f"{quote(f'plugins/{self._user_id}/' + (name or path), safe='')}"
        with open(path, 'br') as f:
            resp = requests.post(url, data=f.read(), headers={
                "Authorization": "Bearer " + self._id_token,
            })
            if not resp.ok:
                raise Exception(resp.text)
