def train(jsondata):
    # 移除以下行，因為不再從本地文件讀取
    # filename = 'C:/Users/shawn/3D Objects/shawn064/shawn0604/學習分析(1205)/result.json'
    # raw = pd.read_json(filename, encoding='utf-8')

    # 使用傳入的 JSON 數據
    raw = pd.DataFrame(jsondata)

    # field_value 應該從 API 請求中獲取，而不是從用戶輸入
    # field_value = input("Enter the field value: ")

    # 假設 jsondata 中有一個 'field' 鍵用於此目的
    field_value = jsondata.get('field', None)

    # Filter data based on the user input
    filtered_data = raw[raw['field'] == field_value]

    # Tokenize the "review" text
    tokenized_documents_R1 = []
    for document in filtered_data['review']:
        tokens = nltk.word_tokenize(document)
        tokenized_documents_R1.append(" ".join(tokens))

    # Use English stopwords
    from nltk.corpus import stopwords
    english_stopwords = set(stopwords.words('english'))

    # Filter out English stopwords
    tokenized_documents_R1 = [
        " ".join([word for word in doc.split() if word.lower() not in english_stopwords])
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
    edges = [(row['word1'], row['word2']) for _, row in df_part.iterrows()]
    weights = list(df_part['weight'])

    G = nx.Graph()

    for edge in edges:
        G.add_node(edge[0])
        G.add_node(edge[1])
        G.add_edge(edge[0], edge[1])

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
    # plt.show()
    plt.savefig('static/graph5.png')

