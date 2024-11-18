from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import plotly.express as px
from igraph import Graph as iGraph

app = Flask(__name__)

# Функція для обчислення TF-IDF
def calculate_tfidf(texts):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    df = pd.DataFrame(dense, columns=feature_names)
    return df, feature_names

# Роут для головної сторінки
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Отримання введеного тексту
        input_texts = request.form["texts"].split("\n")
        # Розрахунок TF-IDF
        tfidf_df, feature_names = calculate_tfidf(input_texts)

        # Вибір ключових фраз (топ-10 для кожного тексту)
        key_phrases = {}
        for idx, row in tfidf_df.iterrows():
            top_features = row.sort_values(ascending=False).head(10).index.tolist()
            key_phrases[f"Text {idx+1}"] = top_features

        # Побудова графіка з Plotly
        top_phrases = tfidf_df.sum(axis=0).sort_values(ascending=False).head(10)
        fig = px.bar(
            x=top_phrases.index,
            y=top_phrases.values,
            labels={"x": "Ключові фрази", "y": "TF-IDF оцінка"},
            title="10 найчастіших фраз"
        )
        plot_div = fig.to_html(full_html=False)

        # Побудова графа з iGraph
        g = iGraph(directed=False)
        all_phrases = list(top_phrases.index)
        g.add_vertices(all_phrases)
        edges = [(all_phrases[i], all_phrases[j]) for i in range(len(all_phrases)) for j in range(i+1, len(all_phrases))]
        g.add_edges(edges)
        graph_data = {
            "vertices": g.vs["name"],
            "edges": [(edge.source, edge.target) for edge in g.es],
        }

        return render_template(
            "index.html",
            plot_div=plot_div,
            key_phrases=key_phrases,
            graph_data=graph_data,
        )

    return render_template("index.html")

# Запуск Flask-сервера
if __name__ == "__main__":
    app.run(debug=True)
