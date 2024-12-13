import requests
import pandas as pd


class MatchDataHandler:
    def __init__(self, url, my_college = False):
        self.url = url
        self.my_college = my_college

    def main_workflow(self):
        self.df = self.get_responses()
        if self.df.shape[0] == 0:
            return None
        
        if self.my_college:
            self.filter_my_college()
        
        df_dict = {}
        for index, row in self.df.iterrows():
            row_df = pd.DataFrame([row])
            row_df, key = self.get_filtered_df(row_df)
            df_dict[key] = row_df

        return df_dict

    def filter_my_college(self):
        self.df = self.df[ (self.df['team1'] == 'IIT MANDI') | (self.df['team2'] == 'IIT MANDI' ) ]

    def get_responses(self):
        response = requests.get(self.url)
        response.raise_for_status()
        data = response.json().get('matches', [])
        return pd.DataFrame(data)

    def get_filtered_df(self, df):
        category = str(df['category'].values[0])
        time_val = str(df['time'].values[0])
        date_val = str(df['date'].values[0])[:10]
        match_id = str(df['matchId'].values[0])

        final_str = f"{category} | {time_val} | {date_val} |{match_id}"
        relevant_columns = ['team1', 'set1_score1', 'set2_score1', 'set3_score1', 'set4_score1', 'set5_score1',
                            'team2', 'set1_score2', 'set2_score2', 'set3_score2', 'set4_score2', 'set5_score2']

        relevant_columns = [x for x in relevant_columns if x in df.columns]
        if len(relevant_columns) > 2:
            df = df[relevant_columns]
        
            df = pd.DataFrame(
                [df.values.flatten()[:6], df.values.flatten()[6:]],
                columns=['Team', 'Set 1', 'Set 2', 'Set 3', 'Set 4', 'Set 5']
            )
        
        df.fillna(0, inplace=True)
        return df, final_str

    
