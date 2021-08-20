class DataModel:
    def __init__(self, post_id, url, author_name, subreddit,
                 post_title, post_text, post_text_embedding,
                 post_length, num_votes, is_nsfw, num_comments,
                 num_shares, post_timestamp, exec_time):
        self.post_id = post_id
        self.url = url
        self.author_name = author_name
        self.subreddit = subreddit
        self.post_title = post_title
        self.post_text = post_text
        self.post_text_embedding = post_text_embedding
        self.post_length = post_length
        self.num_votes = num_votes
        self.is_nsfw = is_nsfw
        self.num_comments = num_comments
        self.num_shares = num_shares
        self.post_timestamp = post_timestamp
        self.exec_time = exec_time

    def to_dict(self):
        data = {'post_id': self.post_id,
                'url': self.url,
                'author_name': self.author_name,
                'subreddit_name': self.subreddit,
                'post_title': self.post_title,
                'post_text': self.post_text,
                'post_text_embedding': self.post_text_embedding,
                'post_length': self.post_length,
                'num_votes': self.num_votes,
                'is_nsfw': self.is_nsfw,
                'num_comments': self.num_comments,
                'num_shares': self.num_shares,
                'post_timestamp': self.post_timestamp,
                'exec_time': self.exec_time}

        return data
