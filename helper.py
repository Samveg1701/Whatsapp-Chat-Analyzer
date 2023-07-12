def fetch_stats(selected_user,df):
    if selected_user == 'overall':
        return df.shape
