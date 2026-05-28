import pandas as pd
import plotly.express as px


def create_department_chart():

    data = {
        "Department": [
            "Risk",
            "Compliance",
            "IT"
        ],

        "Documents": [
            18,
            12,
            9
        ]
    }

    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Department",
        y="Documents",
        text="Documents",
        title="Document Distribution by Department",
        template="plotly"
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0
    )

    fig.update_layout(
        height=420,

        title_font_size=22,

        paper_bgcolor="white",

        plot_bgcolor="white",

        font=dict(
            color="#0f172a",
            size=14
        ),

        xaxis=dict(
            showgrid=False
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="#374151"
        )
    )

    return fig