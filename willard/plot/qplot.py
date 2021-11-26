import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from willard.type import qreg


class qplot:
    def __init__(self, qr: qreg) -> None:
        self.qr = qr
        self.fig = make_subplots(specs=[[{"secondary_y": True}]])
        self.tags = []

    def add(self, tag):
        y_probs = self.qr.state.abs().square().T.squeeze().cpu().numpy()
        y_phases = (self.qr.state.angle() + 2 * np.pi) % (2 * np.pi)
        y_phases *= 180 / np.pi
        y_phases = y_phases.T.squeeze().cpu().numpy()
        x = [bin(i).replace("0b", "").zfill(len(self.qr))
             for i in range(2 ** len(self.qr))]
        self.tags.append(tag)

        self.fig.add_trace(go.Bar(
            visible=False,
            x=x,
            y=y_probs,
            width=0.5,
            name="Probability"),
            secondary_y=False,
        )
        self.fig.add_trace(go.Scatter(
            visible=False,
            x=x,
            y=y_phases,
            line_shape='hvh',
            name="Phase"),
            secondary_y=True,
        )

    def show(self):
        # Make 0th trace visible
        self.fig.data[0].visible = True
        self.fig.data[1].visible = True

        # Create and add slider
        steps = []
        for i, tag in enumerate(self.tags):
            step = dict(
                method="update",
                args=[{"visible": [False] * (len(self.tags) * 2)},
                      {"title": "[<b>Qreg visualization</b>] Tag: " + tag}],
            )
            # Toggle i'th trace to "visible"
            step["args"][0]["visible"][i * 2] = True
            step["args"][0]["visible"][i * 2 + 1] = True
            step['label'] = tag
            steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Current: "},
            pad={"t": 50},
            steps=steps
        )]

        # Add figure title
        self.fig.update_layout(
            sliders=sliders,
            title="[<b>Qreg visualization</b>] Tag: " + self.tags[0],
            template="plotly_dark"
        )

        # Set x-axis title
        self.fig.update_xaxes(title_text="<b>Binary Value</b>")

        # Set y-axes titles
        self.fig.update_yaxes(title_text="<b>Probability</b>", secondary_y=False,
                              range=[0., 1.], linecolor='midnightblue', gridcolor='midnightblue')
        self.fig.update_yaxes(title_text="<b>Phase</b>", secondary_y=True,
                              range=[0, 360], linecolor='maroon', gridcolor='maroon')
        self.fig.show()


def plot_qreg(qr: qreg) -> None:
    y_probs = qr.state.abs().square().T.squeeze().numpy()
    y_phases = (qr.state.angle() + 2 * np.pi) % (2 * np.pi)
    y_phases = y_phases.T.squeeze().numpy()
    x = [bin(i).replace("0b", "").zfill(qr.size)
         for i in range(2 ** qr.size)]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=x,
        y=y_probs,
        name="Probability",
        smoothing=1.3,),
        secondary_y=False,
    )
    fig.add_trace(go.Scatter(
        x=x,
        y=y_phases,
        name="Phase"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="<b>Qreg visualization</b>",
        template="plotly_dark"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="<b>Binary Value</b>")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Probability</b>", secondary_y=False,
                     range=[0., 1.], linecolor='midnightblue', gridcolor='midnightblue')
    fig.update_yaxes(title_text="<b>Phase</b>", secondary_y=True,
                     range=[0, 2 * np.pi], linecolor='maroon', gridcolor='maroon')

    fig.show()
