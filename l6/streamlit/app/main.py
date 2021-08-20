import requests
import streamlit as st


st.title("Streamlit app")

option = st.selectbox(
    'Which model would you like to use?',
    ('linear regressor', 'binary classificator', 'multiclass classificator')
)

st.write('You selected:', option)

if option == 'linear regressor':
    # inputCols=['subreddit_name_numeric', 'num_votes', 'is_nsfw_numeric',
    #            'num_comments', 'num_shares', 'post_text_embedding_vector']
    # labelCol='post_length'
    endpoint = '/lr_model'

    # subreddit_name = st.text_input('Subreddit name:', '')
    subreddit_name = st.selectbox(
        'Subreddit:',
        ('AskReddit', 'food', 'pics', 'worldnews', 'funny')
    )
    post_title = st.text_input('Post title:', '')
    post_text = st.text_input('Post text:', '')
    # is_nsfw = st.text_input('Is NSFW:', '')
    is_nsfw = st.selectbox(
        'Is NSFW:',
        ('True', 'False')
    )
    num_votes = st.text_input('Number of votes:', '')
    num_comments = st.text_input('Number of comments:', '')
    num_shares = st.text_input('Number of shares:', '')
    text_to_embedded = post_title + ' ' + post_text

    params = {
        'subreddit_name': subreddit_name, 
        'num_votes': num_votes, 
        'is_nsfw': is_nsfw, 
        'num_comments': num_comments, 
        'num_shares': num_shares, 
        'post_text_embedding' : text_to_embedded
    }

    st.write('Predicted post length:')

elif option == 'binary classificator':
    # inputCols=['subreddit_name_numeric', 'post_length', 'num_votes',
    #            'num_comments', 'num_shares', 'post_text_embedding_vector']
    # labelCol='is_nsfw_numeric'
    endpoint = '/bc_model'

    # subreddit_name = st.text_input('Subreddit name:', '')
    subreddit_name = st.selectbox(
        'Subreddit:',
        ('AskReddit', 'food', 'pics', 'worldnews', 'funny')
    )
    post_title = st.text_input('Post title:', '')
    post_text = st.text_input('Post text:', '')
    # post_length = st.text_input('Post length:', '')
    post_length = len(post_title) + len(post_text)
    num_votes = st.text_input('Number of votes:', '')
    num_comments = st.text_input('Number of comments:', '')
    num_shares = st.text_input('Number of shares:', '')
    text_to_embedded = post_title + ' ' + post_text

    params = {
        'subreddit_name': subreddit_name, 
        'post_length': post_length, 
        'num_votes': num_votes, 
        'num_comments': num_comments, 
        'num_shares': num_shares, 
        'post_text_embedding' : text_to_embedded
    }

    st.write('Predicted is NSFW (numeric):')

elif option == 'multiclass classificator':
    # inputCols=['is_nsfw_numeric', 'post_length', 'num_votes',
    #            'num_comments', 'num_shares', 'post_text_embedding_vector']
    # labelCol='subreddit_name_numeric'
    endpoint = '/mc_model'

    post_title = st.text_input('Post title:', '')
    post_text = st.text_input('Post text:', '')
    # post_length = st.text_input('Post length:', '')
    post_length = len(post_title) + len(post_text)
    # is_nsfw = st.text_input('Is NSFW:', '')
    is_nsfw = st.selectbox(
        'Is NSFW:',
        ('True', 'False')
    )
    num_votes = st.text_input('Number of votes:', '')
    num_comments = st.text_input('Number of comments:', '')
    num_shares = st.text_input('Number of shares:', '')
    text_to_embedded = post_title + ' ' + post_text

    params = {
        'is_nsfw': is_nsfw, 
        'post_length': post_length,
        'num_votes': num_votes, 
        'num_comments': num_comments, 
        'num_shares': num_shares, 
        'post_text_embedding' : text_to_embedded
    }

    st.write('Predicted subreddit name (numeric):')


submit = st.button('Get prediction')
if submit:
    model_url = 'http://flask-spark:8080' + endpoint
    requests_output = requests.get(model_url, params=params)
    st.write(requests_output.text)