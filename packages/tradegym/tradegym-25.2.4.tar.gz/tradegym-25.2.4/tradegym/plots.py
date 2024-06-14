import os
import io
import pandas as pd
import plotly
import plotly.io as pio
from plotly.graph_objs import Figure, Scatter
from IPython.display import display, Image
from typing import Optional


class Plotter:
    def __init__(self, report_folder: str = './backtest_reports/'):
        self.report_folder = report_folder
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)

    def _get_plotly_fig(self, data: pd.DataFrame, template: str = 'plotly_dark', title: str = "Weights", xaxis_title: str = 'Date', yaxis_title: str = 'Weight') -> Figure:
        """Create a Plotly figure.

        Args:
            data (pd.DataFrame): Data for the plot.
            template (str, optional): Plotly template. Defaults to 'plotly_dark'.
            title (str, optional): Title of the plot. Defaults to "Weights".
            xaxis_title (str, optional): Title of the x-axis. Defaults to 'Date'.
            yaxis_title (str, optional): Title of the y-axis. Defaults to 'Weight'.

        Returns:
            plotly.graph_objs.Figure: Plotly figure.
        """
        traces = [Scatter(x=data.index, y=data[column], mode='lines', name=column) for column in data.columns]
        layout = plotly.graph_objs.Layout(title=title, xaxis=dict(title=xaxis_title), yaxis=dict(title=yaxis_title))
        fig = plotly.graph_objs.Figure(data=traces, layout=layout)
        fig.update_layout(template=template)
        return fig

    def plot_and_save(self, fig: Figure, plot_png: bool, save_report: bool, filename: str, width: int, height: int, dpi: int) -> None:
        """Helper method to plot, save as PNG, and save as HTML.

        Args:
            fig (Figure): Plotly figure to plot.
            plot_png (bool): Whether to save the plot as PNG.
            save_report (bool): Whether to save the plot as HTML.
            filename (str): Filename for saving the plot.
            width (int): Width of the plot.
            height (int): Height of the plot.
            dpi (int): DPI of the plot.
        """
        if plot_png:
            self.plot_png(fig, width=width, height=height, dpi=dpi)
        else:
            fig.show()
        if save_report:
            self.plot_to_html(fig, filename=filename)

    def plot_to_html(self, fig: Figure, filename: str) -> None:
        """Save the plot as an HTML file.

        Args:
            fig (Figure): Plotly figure to save.
            filename (str): Filename for the HTML file.
        """
        plotly.offline.plot(fig, filename=os.path.join(self.report_folder, filename + '.html'), auto_open=False)

    def plot_png(self, fig: Figure, width: int = 1200, height: int = 600, dpi: int = 100) -> None:
        """Save the plot as a PNG file.

        Args:
            fig (Figure): Plotly figure to save.
            width (int, optional): Width of the PNG. Defaults to 1200.
            height (int, optional): Height of the PNG. Defaults to 600.
            dpi (int, optional): DPI of the PNG. Defaults to 100.
        """
        buf = io.BytesIO()
        pio.write_image(fig, buf, format='png', width=width, height=height, scale=dpi / 100.0)
        buf.seek(0)
        display(Image(data=buf.read(), format='png'))
        buf.close()

    def get_plot_profit_benchmark(self, profit_benchmark: pd.DataFrame, template: str = 'plotly_dark') -> Figure:
        """Get the plot for profit benchmark.

        Args:
            profit_benchmark (pd.DataFrame): DataFrame containing profit benchmark data.
            template (str, optional): Plotly template. Defaults to 'plotly_dark'.

        Returns:
            plotly.graph_objs.Figure: Plotly figure.
        """
        traces = []
        for column in profit_benchmark.columns:
            if column == 'Strategy':
                traces.append(Scatter(x=profit_benchmark.index, 
                                    y=profit_benchmark[column], 
                                    mode='lines', 
                                    name=column, 
                                    line=dict(color='green', width=3)))
            else:
                traces.append(Scatter(x=profit_benchmark.index, 
                                    y=profit_benchmark[column], 
                                    mode='lines', 
                                    name=column, 
                                    line=dict(width=1), 
                                    opacity=0.3))  # Adding opacity for transparency
        layout = plotly.graph_objs.Layout(title='Top Coins vs Strategy by Profit', 
                                        xaxis=dict(title='Date'), 
                                        yaxis=dict(title='Profit $'), 
                                        template=template)
        fig = plotly.graph_objs.Figure(data=traces, layout=layout)
        return fig



    def get_plot_drawdowns_benchmark(self, profit_benchmark: pd.DataFrame, template: str = 'plotly_dark') -> Figure:
        """Get the plot for drawdowns benchmark.

        Args:
            profit_benchmark (pd.DataFrame): DataFrame containing profit benchmark data.
            template (str, optional): Plotly template. Defaults to 'plotly_dark'.

        Returns:
            plotly.graph_objs.Figure: Plotly figure.
        """
        profit_benchmark = profit_benchmark + profit_benchmark.iloc[0]
        cummax = profit_benchmark.cummax()
        drawdowns_percent = ((profit_benchmark - cummax) / cummax) * 100
        traces = [Scatter(x=drawdowns_percent.index, y=drawdowns_percent[column], fill='tozeroy', name=column) for column in drawdowns_percent.columns]
        layout = plotly.graph_objs.Layout(title='Underwater Drawdowns', template=template, xaxis=dict(title='Date'), yaxis=dict(title='Drawdowns %'))
        fig = plotly.graph_objs.Figure(traces, layout=layout)
        return fig

    def get_plot_actions(self, df: pd.DataFrame, template: str = 'plotly_dark') -> Figure:
        """Get the plot for actions.

        Args:
            df (pd.DataFrame): DataFrame containing actions data.
            template (str, optional): Plotly template. Defaults to 'plotly_dark'.

        Returns:
            plotly.graph_objs.Figure: Plotly figure.
        """
        return self._get_plotly_fig(data=df, template=template, title='Actions')

    def get_plot_portfolio_weights(self, df: pd.DataFrame, template: str = 'plotly_dark') -> Figure:
        """Get the plot for portfolio weights.

        Args:
            df (pd.DataFrame): DataFrame containing portfolio weights data.
            template (str, optional): Plotly template. Defaults to 'plotly_dark'.

        Returns:
            plotly.graph_objs.Figure: Plotly figure.
        """
        return self._get_plotly_fig(data=df, template=template, title='Portfolio Weights')
