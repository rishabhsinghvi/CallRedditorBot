import praw
import praw.exceptions

def split_submission(title):
    return title.split(" ")

def create_message(username, id):
    message = """Hello, {}!


Someone just mentioned you in a post title. 


Click the link to visit that post: https://www.reddit.com/{}""".format(username, id)

    return message

def send_message(reddit, user, message):
    subject = "Someone just mentioned you!"
    
    try:
        redditor = reddit.redditor(user)
        redditor.message(subject, message)
        return True
    except praw.exceptions.APIException: # PRAW throws an APIException if user does not exist
        # Currently, no other way to check whether or not user exists
        return False

def proc_submission(reddit, submission):
    no_reply = ['gctrep', 'wishlist', 'nbarep']
    split_title = split_submission(submission.title.lower())

    for word in split_title:
        if word.startswith("/u/") or word.startswith("u/"): # username strings can start with either /u/ or u/
            message = create_message(word, submission.id)
            send_message(reddit, word, message)
            """if submission.subreddit.display_name.lower() in no_reply: # Don't reply to posts in subreddits in no_reply
                continue
            if success == True: #Only reply to submission if user exists
                try:
                    submission.reply("Called {}.".format(word))
                except praw.exceptions.APIException: # Handle APIException if rate limit exceeded
                    pass
            """
            

def main():
    no_look = ['removalbot', 'debaterightists']
    reddit = praw.Reddit('CallRedditorBot', user_agent='RedditBot v1')

    if reddit==None:
        return
    

    subreddit = reddit.subreddit('all')

    for submission in subreddit.stream.submissions():
        if submission.subreddit.display_name.lower() in no_look:
            continue
        proc_submission(reddit, submission)
    

if __name__ == "__main__":
    main()