import os
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt')
nltk.download('stopwords')

def train(raw, chosen_category):
    filename = 'result.json'
    if os.path.exists(filename):
        # 读取文件
        raw = pd.read_json(filename, encoding='utf-8')
        
        # 根據 chosen_category 過濾數據
        field_value = chosen_category
        
        # Filter data based on the user input
        filtered_data = raw[raw['field'] == field_value]
        
        # Tokenize the "review" text
        tokenized_documents_R1 = [
            " ".join(nltk.word_tokenize(document))
            for document in filtered_data['review']
        ]

        # 合併英文停用詞和中文停用詞
        stopwords_set = set(stopwords.words('english')).union(set(stopwords.words('chinese')))
        
        # 過濾停用詞
        tokenized_documents_R1 = [
            " ".join([word for word in doc.split() if word.lower() not in stopwords_set])
            for doc in tokenized_documents_R1
        ]

        # Create a co-occurrence matrix
        vectorizer = CountVectorizer()
        dtm_R1 = vectorizer.fit_transform(tokenized_documents_R1)
        dtm_R1_Words = vectorizer.get_feature_names_out()
        X = dtm_R1.toarray()
        df_tdm_R1 = pd.DataFrame(X, columns=list(dtm_R1_Words))

        # Calculate the co-occurrence matrix
        X_cooc = df_tdm_R1.T.dot(df_tdm_R1)
        X_coo = X_cooc.stack().reset_index()
        X_coo.columns = ['word1', 'word2', 'weight']
        X_coo_df = X_coo[X_coo['weight'] > 0].reset_index(drop=True)

        arr = X_coo_df['weight']
        median = 3

        df_part = X_coo_df.loc[arr >= median]
        df_part = df_part.reset_index(drop=True)

        # Sort co-occurrence relationships
        df_part = df_part.sort_values(by='weight', ascending=False)

        # Select the top N co-occurrence relationships
        N = 20
        df_part = df_part.head(N)

        # Build the graph
        edges = create_graph(X_cooc, dtm_R1_Words)
        plot_graph(edges)

    else:
        print(f"File '{filename}' does not exist.")

def create_graph(cooc_matrix, words):
    edges = []
    # 遍歷共現矩陣，添加邊
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            weight = cooc_matrix[i, j]
            if weight > 0:
                edges.append((words[i], words[j], weight))
    return edges

def plot_graph(edges):
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])

    # Plot the graph
    fig = plt.figure(figsize=(20, 20))
    pos = nx.kamada_kawai_layout(G)

    node_size = 2000
    node_color = 'skyblue'
    edge_color = 'gray'
    font_size = 14

    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edge_color=edge_color, alpha=0.5, width=2)
    nx.draw_networkx_labels(G, pos, font_size=font_size, font_family='SimSun')

    plt.axis('off')
    plt.savefig('static/graph7.png')
    # plt.show()  # 這裡不需要再顯示，因為已經保存了
    
raw = pd.read_json('result.json', encoding='utf-8')
train(raw, '藝術')

