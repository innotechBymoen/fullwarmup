from flask import Flask, request, Response
import json
import dbinteractions as db
import sys

app = Flask(__name__)


@app.post("/api/post")
def post_blog_post():
    try:
        username = request.json['username']
        content = request.json['content']
        success, id = db.insert_post(username, content)
        if(success):
            post_json = json.dumps({
                "username": username,
                "content": content,
                "id": id
            }, default=str)
            return Response(post_json, mimetype="application/json", status=201)
        else:
            return Response("Invalid Blog Post", mimetype="plain/text", status=400)
    except KeyError:
        return Response("Missing username/content", mimetype="plain/text", status=422)
    except:
        return Response("Sorry please try again later", mimetype="plain/text", status=501)


@app.get("/api/post")
def get_blog_post():
    try:
        success, posts = db.get_all_posts()
        if(success):
            posts_json = json.dumps(posts, default=str)
            return Response(posts_json, mimetype="application/json", status=200)
        else:
            return Response("Sorry, please try again", mimetype="plain/text", status=501)
    except:
        return Response("Sorry, please try again", mimetype="plain/text", status=501)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("You must pass a mode to run this python script. Either testing or production. For example:")
    print("python app.py testing")
    exit()

if(mode == "testing"):
    print("Running in testing mode!")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif(mode == "production"):
    print("Running in production mode")
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5005)
else:
    print("Please run with either testing or production. Example:")
    print("python app.py production")
