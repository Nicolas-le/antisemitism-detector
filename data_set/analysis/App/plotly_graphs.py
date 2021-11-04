import plotly.graph_objects as go
import App.data_preprocessing


class Plotting():

    def __init__(self, time_interval, retrieval):
        self.retrieval = retrieval
        self.time_interval = time_interval
        self.extracted_information = self.get_info_dict()
        #self.plot_layout = go.Layout(autosize=False, width=800, height=500)
        self.plot_layout = go.Layout(font=dict(
                                        size=17,
                                    ))
        self.topic_plot = self.create_topic_plot()
        self.counting_plots = self.create_counting_plots()
        self.keyword_distr_plots = self.create_keyword_distr_plot()

    def get_info_dict(self):
        def get_sortable_int_daily(date):
            return int(date[3:5])

        def get_sortable_int_hourly(date):
            return (int(date[3:5]), int(date[13:]))

        info_dict = App.data_preprocessing.preprocess_post_per_time_interval(self.retrieval, self.time_interval)

        if self.time_interval == "daily":
            sorted_info_dict = dict(sorted(info_dict.items(), key=lambda item: get_sortable_int_daily(item[0])))
        else:
            sorted_info_dict = dict(sorted(info_dict.items(), key=lambda item: (get_sortable_int_hourly(item[0])[0], get_sortable_int_hourly(item[0])[1])))

        return sorted_info_dict

    def write_plot(self, fig, name):
        fig.write_image("./plots/" + name + ".png")

    def show_plot(self, fig):
        fig.show()

    def create_topic_plot(self):

        def build_topic_list():
            all_topics = []
            for date, value in self.extracted_information.items():
                for day_topic in value["topic_distr"]:
                    all_topics.append(day_topic[0])
            return list(set(all_topics))

        all_topics = build_topic_list()
        data = []


        for topic in all_topics:
            dates = []
            values = []
            for date, value in self.extracted_information.items():
                if date == "05/07/21(Fri)":
                    continue
                for day_topic in value["topic_distr"]:
                    topic_appeared = False

                    if topic == day_topic[0]:
                        dates.append(date)
                        values.append(day_topic[1])
                        topic_appeared = True

                    if not topic_appeared:
                        dates.append(date)
                        values.append(0)

            data.append(go.Bar(name=topic, x=dates, y=values))


        fig = go.Figure(data=data, layout= self.plot_layout)
        fig.update_layout(barmode='stack')
        fig.update_xaxes(title_text="dates")
        fig.update_yaxes(title_text="counts")

        return fig

    def create_counting_plots(self):
        plots = {}
        concepts = {"count_replies": ["count","replies"],
                    "counts": ["word_count_total", "word_count_without_stopwords"]
                    }

        for name, list in concepts.items():
            data = []
            for concept in list:
                dates = []
                values = []
                for date, value in self.extracted_information.items():
                    if date == "05/07/21(Fri)":
                        continue
                    for conc, val in value["countings"]["thread_general"].items():
                        if concept == conc:
                            dates.append(date)
                            values.append(val)

                data.append(go.Bar(name=concept, x=dates, y=values))


            fig = go.Figure(data=data, layout=self.plot_layout)
            fig.update_layout(barmode='group')
            fig.update_xaxes(title_text="dates")
            fig.update_yaxes(title_text="counts")

            plots[name] = fig

        data = []
        for date, value in self.extracted_information.items():
            if date == "05/07/21(Fri)":
                continue
            for thread in value["countings"]["special_threads"]["traffic"]:
                if thread[1] >= 350:
                    data.append(go.Bar(name=thread[0], x=[date], y=[thread[1]]))

        fig = go.Figure(data=data, layout=self.plot_layout)
        fig.update_layout(barmode='stack')
        fig.update_xaxes(title_text="dates")
        fig.update_yaxes(title_text="counts")

        plots["special_threads"] = fig

        return plots

    def create_keyword_distr_plot(self):
        plots = {}

        def create_percentage_plot():
            dates = []
            values = []

            for key, value in self.extracted_information.items():
                if key == "05/07/21(Fri)":
                    continue
                dates.append(key)
                values.append(value["keyword_distr"]["percentage_of_keyword_occ"]*100)

            fig = go.Figure(data=[go.Bar(name="percentage_of_keyword_occ", x=dates, y=values)], layout=self.plot_layout)
            fig.update_layout(barmode='stack')

            return fig

        def create_highest_thread_plot():
            plots = []
            for key, value in self.extracted_information.items():
                if key == "05/07/21(Fri)":
                    continue
                data = []

                for thread, dict in value["keyword_distr"]["highest_threads"].items():
                    keywords = []
                    values = []

                    for keyword, count in dict.items():
                        keywords.append(keyword)
                        values.append(count)

                    data.append(go.Bar(name=thread, x=keywords, y=values))

                fig = go.Figure(data=data, layout=self.plot_layout)
                fig.update_layout(barmode='stack', title=key)

                plots.append(fig)

            return plots

        plots["percentage_of_keyword_occ"] = create_percentage_plot()
        plots["highest_thread_plot"] = create_highest_thread_plot()

        return plots



