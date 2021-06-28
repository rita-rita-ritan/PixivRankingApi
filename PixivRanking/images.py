import json
import falcon

class Resource:
    def on_get(self, req, resp):
        doc = {
            "images": [
                {
                    "href": "hoge.png",
                    "msg": "こちらりたりたバックエンド。"
                }
            ]
        }

        resp.text = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200  # can be omitted because 200 is the default
