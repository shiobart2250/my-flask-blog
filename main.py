from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import(
    UserMixin,
    LoginManager,
    current_user,
    login_user,
    login_required,
    logout_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
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

# Flask-loginの設定
login_manager = LoginManager()
login_manager.init_app(app)
# 未ログイン時にリダイレクトするエンドポイント名
login_manager.login_view = "login"


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

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.username}>"

@app.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    # index.htmlをレンダリング
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post) 

# Flask-Loginがユーザ情報をロードするための関数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.secret_key = "secret"

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
    
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        else:
            flash("ユーザ名またはパスワードが正しくありません")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
