from aws_cdk import aws_cloudwatch as cw

class Bluedac_Dashboard(cw.Dashboard):
    """Bluedac-adapted version of Dashboard provided by AWS CloudWatch.
    This class provides 'append_metrics' method, to comfortably join
    different graphs/texts and compose a dashboard.
    """

    str_to_stat = {
        "average": cw.Stats.AVERAGE,
        "sum": cw.Stats.SUM,
        "maximum": cw.Stats.MAXIMUM,
        "minimum": cw.Stats.MINIMUM,
        "iqm": cw.Stats.IQM,
        "count": cw.Stats.SAMPLE_COUNT
    }
    """Translation map for str -> cw.Stats"""

    def __init__(
        self,
        stack,
        dashboard_name
    ):
        """
        :param stack: The stack where this resource is being deployed to.
        :param dashboard_name: The name of the CloudWatch dashboard.
        """

        super().__init__(stack, dashboard_name)

    def build_with(self, metrics: list):
        """Builds a dashboard using a list of graphs/texts to a CloudWatch Dashboard.
        :param metrics: List of metrics that will be attached to CloudWatch Dashboard.
        """

        for metric in metrics:
            match metric["type"]:
                case "TextWidget":
                    self.add_widgets(
                        cw.TextWidget (
                            markdown = metric["text"],
                            width = 24,
                            height = 2
                        )
                    )
                case "GraphWidget":
                    self.add_widgets(
                        cw.GraphWidget(
                            title=f"Lambda {metric['metric']}",
                            width=8,
                            statistic=Bluedac_Dashboard.str_to_stat[metric["statistic"]],
                            left=[metric["resource"].metric(metric["metric"], period=metric["duration"])]
                        )
                    )
