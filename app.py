import streamlit as st
import pandas as pd
import re
# import string as str
import preprocessor
import urlextract
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji
# import datetime as dt

f = open('C:/Users/asus/Downloads/stop_hinglish.txt', 'r')
stop_words = f.read()
# print(stop_words)

# import helper
from collections import Counter

def emoji(selected_user, df):
    import emoji
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []  # Initialize an empty list to store the emojis

    for message in df['message']:
        message_emojis = [c for c in message if c in emoji.UNICODE_EMOJI['en']]  # Extract emojis from the message
        emojis.extend(message_emojis)  # Add the extracted emojis to the main list

    print(emojis)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # joined_df

    timeline_data = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline_data.shape[0]):
        time.append(timeline_data['month'][i] + '-' + str(timeline_data['year'][i]))
    timeline_data['time'] = time

    df['daily_activity'] = df['message_date'].dt.date
    daily_timeline = df.groupby('daily_activity').count()['message'].reset_index()

    return timeline_data, daily_timeline, df['day_name'].value_counts(), df['month'].value_counts()



def most_commn_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = []
    with open('C:/Users/asus/Downloads/stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words and word not in [r'[', '\u200egif' ,'meet', r'u200egif', r'omitted', '\u200eimage', '\u200esticker', r'join', r'meeting', '\u200e[','hain.','hai.']:
                words.append(word)

    most_common_word = pd.DataFrame(Counter(words).most_common(20))
    print(most_common_word)
    return most_common_word

# Assuming 'joined_df' is the DataFrame you want to process
# word(joined_df)


def wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    condition = (df['message'] == '‎video omitted\n[') | (df['message'] == '‎image omitted\n[') | (
                df['message'] == 'GIF omitted\n[')

    # def remove_stop_words(message):
    #     # y = []
    #     words = []
    #     with open('C:/Users/asus/Downloads/stop_hinglish.txt', 'r') as f:
    #         stop_words = f.read()
    #
    #     for message in df['message']:
    #         for word in message.lower().split():
    #             if word not in stop_words and word not in [r'[', '\u200egif', 'meet', r'u200egif', r'omitted',
    #                                                        '\u200eimage', '\u200esticker', r'join', r'meeting',
    #                                                        '\u200e[', 'hain.', 'hai.']:
    #                 words.append(word)
    #     return " ".join(word)
    #
    # df['message'] = df['message'].apply(remove_stop_words)

    df = df[~condition]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=""))
    return df_wc


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[(df['message'] == '‎video omitted\n[') | (df['message'] == '‎image omitted\n[') | (
                df['message'] == 'GIF omitted\n[')].shape[0]

    # links = []
    # for message in df['message']:
    #     links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages  # , len(links)


def fetch_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(100 * (df['user'].value_counts() / df.shape[0]), 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})
    return x, df


def preprocess_data(data):
    # pattern =
    pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2} [AP]M'

    messages = re.split(pattern, data)[1:]
    # messages
    # dates = re.findall(pattern, data)
    # dates
    dates = re.findall(pattern, data)[1:]

    df = pd.DataFrame({'message_date': dates})
    df2 = pd.DataFrame({'user_messages': messages})
    # df2

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p')

    df['year'] = df['message_date'].dt.year
    # df['year']
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['month_num'] = df['message_date'].dt.month
    df['day_name'] = df['message_date'].dt.day_name()

    df['minute'] = df['message_date'].dt.minute
    df.head()

    joined_df = pd.concat([df.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)
    print(joined_df)

    users = []
    messages = []
    for message in joined_df['user_messages']:
        entry = re.split(r'(?<!:):\s', message)  # re.split(, string, maxsplit=1)
        if (entry[1:]):
            users.append(entry[0])
            messages.append(entry[1])

    joined_df['user'] = users
    joined_df['message'] = messages
    joined_df.drop(columns=['user_messages'], inplace=True)
    joined_df.sample(10)
    print(joined_df['user'].value_counts())
    # joined_df.drop(columns=['user_messages'], inplace=True)

    # joined_df.sample(10)
    # joined_df['user'].value_counts()

    return joined_df
    # print(df2.head())
    # df = pd.concat([df, df2], ignore_index=True)

    # return df

def period(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    periods = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            periods.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            periods.append(str('00') + "-" + str(hour+1))
        else:
            periods.append(str(hour) + "-" + str(hour+1))

    df['periods'] = periods
    return df

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is None:
    uploaded_file = open('C:/Users/asus/Downloads/_chat.txt', 'r', encoding='utf-8')
if uploaded_file is not None:
    # To read file as bytes:
    # bytes_data = uploaded_file.getvalue()
    data = uploaded_file.read()
    # st.text(data)
    df = preprocess_data(data)
    print(df)
    # st.dataframe(df)
    # print(df.head)
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages = fetch_stats(selected_user, df)  # links var
        st.title("Top Stats")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Shared Media")
            st.title(num_media_messages)
        # with col4:
        #     st.header("Total links")
        #     st.title(links)

    if selected_user == 'Overall':
        st.title('Most active users')
        x, new_df = fetch_busy_users(df)
        col1, col2 = st.columns(2)
        fig, ax = plt.subplots()

        # Create the pie chart
        fig2, ax2 = plt.subplots()
        ax2.pie(new_df['percent'], labels=new_df['name'], autopct='%1.1f%%')

        # Set aspect ratio to be equal so that pie is drawn as a circle
        ax2.axis('equal')

        # labels = new_df['name']
        # values = new_df['percent']

        with col1:
            ax.bar(x.index, x.values)
            fig.set_size_inches(10, 8)
            st.pyplot(fig)
        with col2:
            # st.dataframe(new_df)
            # Add a title
            ax2.set_title('Activity %')
            fig2.set_size_inches(10, 8)

            # Display the plot using Streamlit
            st.pyplot(fig2)

    # bytes_data = uploaded_file.getvalue()
    # data = bytes_data.decode("utf-8")
    # df = preprocessor.preprocess(data)
    # st.dataframe(df)

    #Wordcloud
    st.title("Wordcloud")
    df_wc = wordcloud(selected_user, df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    word_df = most_commn_words(selected_user,df)

    fig, ax = plt.subplots()
    ax.barh(word_df[0],word_df[1])
    # plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)

    # st.dataframe(word_df)

    #emoji
    emoji_df = emoji(selected_user,df)
    st.title("Emoji Analysis ")
    st.dataframe(emoji_df)

    # df['month_num'] = df['message_date'].dt.month
    # df.groupby(['year', 'month_num']).count()['message']

    # if selected_user != 'Overall':
    #     df = df[df['user'] == selected_user]
    #
    # # joined_df
    #
    # timeline_data = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    #
    # time = []
    # for i in range(timeline_data.shape[0]):
    #     time.append(timeline_data['month'][i] + '-' + str(timeline_data['year'][i]))
    # timeline_data['time'] = time




    st.title("Monthly Activity")
    timeline_data, daily_timelne, weekly_timeline, month = monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline_data['time'], timeline_data['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Daily Messages")
    fig, ax = plt.subplots()
    ax.plot(daily_timelne['daily_activity'], daily_timelne['message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Activity Map")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Most busy day")
        fig, ax = plt.subplots()
        ax.bar(weekly_timeline.index, weekly_timeline.values, color='black')
        # plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most busy month")
        fig, ax = plt.subplots()
        ax.bar(month.index, month.values, color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    import seaborn as sns
    period_df = period(selected_user, df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(period_df.pivot_table(index='day_name', columns='periods', values = 'message', aggfunc = 'count').fillna(0))
    plt.figure(figsize=(20,6))
    st.pyplot(fig)
    # plt.yticks(rotation = 'horizontal')
    # plt.show()


