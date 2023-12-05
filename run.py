from uagents import Agent, Context
import requests

NEWS_API_KEY = "012ffdcd6eda49b497154e2cd24bef"
NEWS_API_BASE_URL = "https://newsapi.org/v2/top-headlines"
USER_INTERESTS = ["world", "technology", "sports"]


class NewsAgent(Agent):
    def __init__(self, name, seed):
        super().__init__(name=name, seed=seed)
        self.significant_news = []

    async def fetch_news(self, ctx: Context):
        try:
            params = {
                "apiKey": NEWS_API_KEY,
                "category": ",".join(USER_INTERESTS),
            }

            response = requests.get(NEWS_API_BASE_URL, params=params)
            response.raise_for_status()

            news_data = response.json()

            ctx.logger.info("News fetched successfully!")

        except requests.RequestException as e:
            ctx.logger.error(f"Error fetching news: {e}")

    async def present_news(self, ctx: Context):
        try:
            ctx.logger.info("News presented successfully!")

        except Exception as e:
            ctx.logger.error(f"Error presenting news: {e}")


news_agent = NewsAgent(name="news_agent", seed="news_agent_recovery_phrase")
Agent.register_periodic_task(news_agent.fetch_news, period=60 * 60)
Agent.register_periodic_task(news_agent.present_news, period=24 * 60 * 60)

# Start the agent
news_agent.run()
