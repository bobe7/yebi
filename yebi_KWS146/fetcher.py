# -*- coding: utf-8 -*-
import twitter


class TwitterFetcher:
    def __init__(self):
        self.twitter = twitter.Twitter(
            auth=twitter.OAuth( #트위터 계정인증
                "2901343172-xFtNRQc8SdbZY5WMCVJxVHcq6Y6nvIHshgOEgMQ",
                "tCVvdUav95DKOxRR6BI3zqxrqO2Hzpft54h7Phw4uOM1l",
                "goupuZ0pPcpgFyPDRK3q6qVDe",
                "3ZOmXF82V1pclqnuqN6rgkQ1WWURV1xLjLdkORsfWUb6vvhTw5"))

    def get_time_line(self, no):
        return self.twitter.statuses.home_timeline(count=no)