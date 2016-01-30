# get action
# get sysargs(blog title)

# make or create directory with slugified version of directory
# put meta txt file with topic / category / etc
# open up a vim with title as current time 21:33_2-Jan-2014.md in that directory

import config
import os, sys, datetime
from subprocess import call

EDITOR = os.environ.get('EDITOR','vim')
ACTIONS = ['start', 'generate', 'sync', 'serve']
BLOG_SOURCE_DIR = config.BLOG_SOURCE_DIR

# utils
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
# utils
def get_index(index, _list):
    try:
        return _list[index]
    except IndexError:
        return None

# start
def start(title=None, meta=None):
    """
    prepares directory and shoots up a vim instance with the 
    timing data as a file name.
    whatever goes into the file, later turns into a 
    timestamped text block (for the corresponding `title`).
    """
    # ensure source directory exists
    ensure_dir(BLOG_SOURCE_DIR)
    slugified_title = title.replace(' ', '-')

    now = datetime.datetime.now()
    time_stamp = now.strftime('%b-%d-%Y_%I-%M-%p')
    slugified_title = slugified_title or time_stamp

    # let there be a directory to put the sources in. 
    cwd = os.path.join(BLOG_SOURCE_DIR, slugified_title)
    ensure_dir(cwd)

    # now that the directory is there, open up a vim instance with 
    # title as current datetime and exit.
    call([EDITOR, os.path.join(cwd, time_stamp+'.md')])


#generate
def generate_posts():
    """
    compiles posts from source directory to markdown files
    """
    ensure_dir(config.BLOG_OUT_DIR)


    # directories in source_dir
    post_dirs = [os.path.join(BLOG_SOURCE_DIR, title) 
                    for title in os.listdir(BLOG_SOURCE_DIR) 
                        if os.path.isdir(os.path.join(BLOG_SOURCE_DIR, title))]

    for post_dir in post_dirs:
        blocks = []
        content = ''
        post_dirname = os.path.basename(post_dir)
        title = post_dirname.replace('-', ' ')
        
        # iterate through each file and generate post
        timestamped_files = [os.path.join(post_dir, timestamp)
                                 for timestamp in os.listdir(post_dir) 
                                    if os.path.isfile(
                                        os.path.join(post_dir, timestamp)
                                    )]
        
        for path in timestamped_files:
            timestamp = os.path.splitext(os.path.basename(path))[0]
            with open(path, 'r') as f:
                block = f.read()
            
            blocks.append({
                    'timestamp': timestamp.replace('_', ' '),
                    'block': block
                })


        for block in blocks:
            content = '{content} \n`{timestamp}`: {block}'.format(
                content = content, 
                timestamp = block['timestamp'], 
                block = block['block'])

        content = '####{title} \n {remaining_content}'.format(
            title = title,
            remaining_content = content)

        with open(os.path.join(
                    config.BLOG_OUT_DIR, 
                    post_dirname+'.txt'), 'w') as f:
            f.write(content)


if __name__ == '__main__':
    """
    routes action param to corresponding routines
    """
    
    action = get_index(1, sys.argv).strip()
    if not action:
        print "Please specify an action: " + ' '.join(ACTIONS)

    if action == 'start':
        title = get_index(2, sys.argv).strip()
        meta = get_index(3, sys.argv)
        start(title=title, meta=meta);
    
    if action == 'generate':
        generate_posts()

    if action == 'serve':
        ensure_dir(config.BLOG_OUT_DIR)
        call('cd {dir} && python -m SimpleHTTPServer -p 3000'.format(
            dir=config.BLOG_OUT_DIR))

