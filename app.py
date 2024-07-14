from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        
        blog_posts = load_blog_posts()
        
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
        
        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
        
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_blog_posts()
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    
    if post is None:
        return "Post not found", 404
    
    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
