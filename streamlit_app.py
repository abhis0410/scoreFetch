import streamlit as st
import datetime
import time
from utils import MatchDataHandler


class StreamlitApp:
    def __init__(self, link_dic, my_college):
        self.link_dic = link_dic
        # st.write(self.link_dic)


    def update_handler(self):
        self.handler = {}
        for key, url in self.link_dic.items():
            x = MatchDataHandler(url, my_college)
            value = x.main_workflow()
            self.handler[key] = value


    def show_placeholder(self, placeholder, tuple_value):
        key = tuple_value[0]
        value = tuple_value[1]
        url = self.link_dic[key]

        with placeholder.expander(label = key, expanded=True):
            st.subheader(f"[{key}]({url})")
            if value is None:
                # st.write("No data available.")
                return

            for match_info, match_df in value.items():
                st.write(match_info)
                st.dataframe(match_df)

    def main(self):
        placeholder1 = st.empty()

        total_phs = len(list(self.link_dic.items()))
        placeholders = [st.empty() for _ in range(total_phs)]
        iteration = 0
        while True:
            iteration += 1
            self.update_handler()
            with placeholder1.container(border= True):
                now = datetime.datetime.now().time().strftime("%H:%M:%S")
                st.write(f"Iteration Count: {iteration} | Timestamp: {now}")

            for i, ph in enumerate(placeholders):
                self.show_placeholder(ph, list(self.handler.items())[i])

            time.sleep(10)  # Wait for 10 seconds before refreshing


if __name__ == "__main__":
    api_links = {
        "Live": "https://iism24.iitk.ac.in/api/getLiveMatches?page=1&limit=100&search=&sportTableName=tabletennis",
        "Completed": "https://iism24.iitk.ac.in/api/getCompletedMatches?page=1&limit=100&search=&sportTableName=tabletennis",
        "Upcoming Matches": "https://iism24.iitk.ac.in/api/Matches?page=1&limit=1000&search=&sportTableName=tabletennis",
    
    }
    my_college = st.checkbox("Show only mandi's", value=True)
    st.write(my_college)

    app = StreamlitApp(api_links, my_college)
    app.main()
