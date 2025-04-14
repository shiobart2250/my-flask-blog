from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# ベースディレクトリ設定(SQLiteのパス指定に使う)
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# ダミーのブロブ記事データ(あとでデータベースに置き換え)
posts ={
    1:{"title": "Flask入門", "content": "Flaskは軽量なPython Webフレームワーク"},
    2:{"title": "Tailwind CSSの基本", "content": "ユーティリティファーストで高速なスタイリングが可能"},
    3:{"titlte": "Pythonの学習方法", "content": "基礎から応用まで、様々な学習リソース有り"},
}

# SQLAlchemyの設定
# データベースファイルのパス指定
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "blog.db")
# パフォーマンストラッキング無効か(推奨)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (False)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Post(db.Model):
    # カラム定義
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # デバッグ用
    # オブジェクトを文字列で表示
    def __repr__(self):
        return f"<Post {self.title}>"

@app.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    # index.htmlをレンダリング
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post) 

if __name__ == "__main__":
    app.run(debug=True)
