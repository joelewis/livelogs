####Live Blogging

A simple tool to log your thoughts and consolidate them as blog posts.  

Disclaimer: This is **not** a blogging engine. All it does is power up your terminal to record your thoughts and generates blog post contents out of them. Hosting them, or copy pasting them into your blogging platform is upto you.

`python blog.py start 'Blog Title / Topic'` - opens up a vim instance. Write your content and `:wq` once done. Keep repeating this for every log on that topic.

`python blog.py generate` - Generates .txt/.md files for each post.

`python blog.py server` - Serves your output posts directory on port 3000. 

Modify options `config.py` as per your choice.