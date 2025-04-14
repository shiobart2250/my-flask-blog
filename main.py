from flask import Flask, render_template, abort

app = Flask(__name__)

# ダミーのブロブ記事データ(あとでデータベースに置き換え)
posts ={
    1:{"title": "Flask入門", "content": "Flaskは軽量なPython Webフレームワーク"},
    2:{"title": "Tailwind CSSの基本", "content": "ユーティリティファーストで高速なスタイリングが可能"},
    3:{"titlte": "Pythonの学習方法", "content": "基礎から応用まで、様々な学習リソース有り"},
}

@app.route("/")
def index():
    # index.htmlをレンダリング
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get(post_id)
    if post is None:
        abort(404)

    return render_template("post.html", post=post) 

if __name__ == "__main__":
    app.run(debug=True)
