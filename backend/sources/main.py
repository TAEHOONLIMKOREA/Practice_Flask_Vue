from flask import Flask, render_template, make_response
import os
app = Flask(__name__
            , template_folder=os.getcwd()+'../../frontend/dist'
            , static_folder=os.getcwd()+'../../frontend/dist/static'
            , static_url_path='/static')

@app.route("/", methods=["GET"])
def page_index():
    resp = make_response(render_template("index.html"))
    return resp

if __name__ == "__main__":
    app.run()