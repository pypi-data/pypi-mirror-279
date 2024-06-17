import nltk  # type: ignore
import matplotlib.pyplot as plt
from chatInsights import _transformData
from wordcloud import WordCloud  # type: ignore
from nltk.corpus import stopwords  # type: ignore


class ChatInsights:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data = _transformData(self.file_path)

    def active_users(self, save_figure: str = "N") -> None:
        plt.figure(figsize=(8, 4))
        m_a = self.data["user"].value_counts().head(10).sort_values()
        m_a.plot.barh(
            color=[
                "#696969",
                "#0ff1ce",
                "#ffd700",
                "#ffff00",
                "#ff0000",
                "#ac25e2",
                "#ff00ff",
                "#00ced1",
                "#008080",
                "#8cff32",
            ]
        )

        for index, value in enumerate(m_a):
            plt.text(
                value + 3, index, str(value), va="center", color="black", fontsize=7
            )

        plt.ylabel("Users")
        plt.xlabel("No. of messages")
        plt.title("Users Activity Stats", fontdict={"fontsize": 11})
        if save_figure == "Y" or save_figure == "y":
            plt.savefig("active_users.png", bbox_inches="tight")
        plt.show()

    def active_day(self, save_figure: str = "N") -> None:
        plt.figure(figsize=(7, 3))
        a_d = self.data["day"].value_counts().head(10).sort_values()
        a_d.plot.barh(
            color=[
                "#8cff32",
                "#0ff1ce",
                "#ffd700",
                "#ffff00",
                "#ff0000",
                "#ac25e2",
                "#ff00ff",
            ]
        )

        for index, value in enumerate(a_d):
            plt.text(
                value + 3, index, str(value), va="center", color="black", fontsize=6
            )

        plt.ylabel("Week Days")
        plt.xlabel("No. of messages")
        plt.title("Weekly Message Stats", fontdict={"fontsize": 11})
        if save_figure == "Y" or save_figure == "y":
            plt.savefig("active_day.png", bbox_inches="tight")
        plt.show()

    def active_month(self, save_figure: str = "N") -> None:
        plt.figure(figsize=(8, 4))
        a_m = self.data["month_year"].value_counts().sort_values()[:10]
        a_m.plot.barh(
            color=[
                "#8cff32",
                "#0ff1ce",
                "#ffd700",
                "#ffff00",
                "#ff0000",
                "#ac25e2",
                "#ff00ff",
                "#00ced1",
                "#008080",
                "#696969",
            ]
        )

        for index, value in enumerate(a_m):
            plt.text(
                value + 3, index, str(value), va="center", color="black", fontsize=7
            )

        plt.ylabel("Months")
        plt.xlabel("No. of messages")
        plt.title("Monthly Message Stats", fontdict={"fontsize": 11})
        if save_figure == "Y" or save_figure == "y":
            plt.savefig("active_month.png", bbox_inches="tight")
        plt.show()

    def active_year(self, save_figure: str = "N") -> None:
        df = self.data["year"].value_counts().to_frame().reset_index()
        plt.figure(figsize=(6, 4))
        bars = plt.bar(df["year"], df["count"], color=["#ffff00", "#ff0000", "#ac25e2"])

        for bar in bars:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 0.1,
                str(int(yval)),
                ha="center",
                va="bottom",
                fontsize=7,
            )

        plt.xlabel("Years")
        plt.ylabel("No. of messages")
        plt.title("Yearly Message Stats", fontdict={"fontsize": 11})
        plt.xticks(df["year"])

        if save_figure == "Y" or save_figure == "y":
            plt.savefig("active_year.png", bbox_inches="tight")

        plt.show()

    def word_cloud(self, save_figure: str = "N") -> None:
        nltk.download("stopwords")

        def _preprocess_text(df):
            hindi = [chr(c) for c in range(0x0900, 0x097F)]
            temp = df[
                ~(df["message"].str.contains("<Media omitted>"))
                & ~(df["message"].str.contains("This message was deleted"))
                & ~(df["message"].str.contains("https://"))
                & ~(df.message.str.contains("|".join(hindi)))
            ]
            txt = " ".join(review for review in temp.message)
            return txt

        text = _preprocess_text(self.data)
        stop_words = set(stopwords.words("english"))
        wordcloud = WordCloud(
            width=1920,
            height=1080,
            background_color="white",
            stopwords=stop_words,
            random_state=42,
            colormap="inferno",
            collocations=False,
        ).generate(text)
        plt.figure(figsize=(6, 3))
        plt.imshow(wordcloud)

        if save_figure == "Y" or save_figure == "y":
            plt.savefig("wordcloud.png")
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()
