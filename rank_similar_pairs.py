import pandas as pd
from itertools import product
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

def rank_similar_pairs(doc_info: pd.DataFrame, model_name="paraphrase-multilingual-MiniLM-L12-v2", threshold=0.8):
    """
    Сравнивает документы между Л2 и Л3 внутри одной темы.
    Возвращает DataFrame с расширенным набором полей для пар текстов и их косинусной близостью.
    """

    model = SentenceTransformer(model_name)

    results = []

    # Добавляем прогресс-бар для отслеживания выполнения
    topics = doc_info.groupby("Тема")
    for topic, group in tqdm(topics, desc="Обработка тем", unit="тема"):
        l2_group = group[group["Рабочая группа"] == "Л2. SAP. Закупки"]
        l3_group = group[group["Рабочая группа"] == "Л3. SAP. Закупки"]

        l2_docs = l2_group["clean_documents"].tolist()
        l3_docs = l3_group["clean_documents"].tolist()

        if not l2_docs or not l3_docs:
            continue

        for d1, d2 in product(l2_docs, l3_docs):
            embeddings = model.encode([d1, d2], normalize_embeddings=True, show_progress_bar=False)
            sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

            if sim >= threshold:
                # Получаем дополнительные поля для текущих строк Л2 и Л3
                l2_row = l2_group[l2_group["clean_documents"] == d1].iloc[0]
                l3_row = l3_group[l3_group["clean_documents"] == d2].iloc[0]

                results.append({
                    "Text_L2": d1,
                    "Text_L3": d2,
                    "Similarity": sim,
                    "Номер Л2": l2_row["Номер"],
                    "Номер Л3": l3_row["Номер"],
                    "Описание Л2": l2_row["Описание"],
                    "Описание Л3": l3_row["Описание"],
                    "Дата регистр. Л2": l2_row["Дата ��егистр."],
                    "Дата регистр. Л3": l3_row["Дата регистр."],
                    "Услуга Л2": l2_row["Услуга"],
                    "Услуга Л3": l3_row["Услуга"]
                })

    result_df = pd.DataFrame(results).sort_values(by="Similarity", ascending=False).reset_index(drop=True)

    return result_df
