import plotly.graph_objects as go

def plot_antisem_proportions(video_dict):
    plot_layout = go.Layout(width=1920, height=1080)

    data = []
    categories = ["antisemitic",
                  "probably_antisemitic",
                  "maybe_antisemitic",
                  "not_antisemitic"]

    for category in categories:
        videos = []
        values = []

        for video_id, video_information in video_dict.items():
            videos.append(video_information["title"])
            values.append(video_information[category])

        data.append(go.Bar(name=category, x=videos, y=values))

    fig = go.Figure(data=data, layout=plot_layout)
    fig.update_layout(barmode='stack')
    fig.update_xaxes(title_text="video_ids")
    fig.update_yaxes(title_text="counts")

    fig.show()
    #fig.write_image("./al_jazeerah.png")


