class BooksRecomender():
    def __init__(self, days=60, item_columns='smart_collapse_field', user_columns='readerID', date='startDate'):
        self.days = days
        self.item_columns = item_columns
        self.user_columns = user_columns
        self.date = date
        
    def cat_proc(self, cat):
        cat['yea'] = cat['yea'].astype(str).str.extract(r'([0-9]+)')
        cat['yea'] = cat['yea'].astype(str).apply(lambda x: x[:4])
        cat['yea'] = cat['yea'].replace('nan','1979')
        cat['aut'] = cat['aut'].fillna('Неизвестно')
        cat['serial'] = cat['serial'].fillna('Неизвестно')
        cat['publ'] = cat['publ'].fillna('Неизвестно')
        cat['biblevel'] = cat['biblevel'].fillna('Неизвестно')
        cat['ager'] = cat['ager'].fillna('12+')
        cat['place'] = cat['place'].fillna('Неизвестно')
#         cat = cat.drop('person', 1)
        cat.id = cat.id.astype(int)
        cat['annotation'] = cat['annotation'].fillna('Отсутствует')
        cat['keyword'] = cat['keyword'].fillna('Отсутствует')
        
        return cat
    
    def circulaton_proc(self, circulaton):
#         circulaton = circulaton.drop('barcode', 1)
        circulaton['startDate'] = pd.to_datetime(circulaton['startDate'], format="%d.%m.%Y")
        circulaton['finishDate'] = pd.to_datetime(circulaton['finishDate'], format="%d.%m.%Y")
        return circulaton
    
    def readers_proc(self, readers):
        readers.columns = ['abis_id', 'dateOfBirth', 'Address', 'Unknown_1', 'Unknown_2']
        readers = readers.drop(columns=['Unknown_1', 'Unknown_2'])
        row = {'abis_id': 366670, 'dateOfBirth': '14.10.1974', 'Address': 'Обручевский, 10'}
        readers = readers.append(row, ignore_index=True)
        readers['Address'] = readers['Address'].fillna('Неизвестно')
        readers['dateOfBirth'] = pd.to_datetime(readers['dateOfBirth'])
        time = readers['dateOfBirth'].mean()
        readers['dateOfBirth'] = readers['dateOfBirth'].fillna(time)
        return readers
    
    def get_coo_matrix(self, df, 
                   user_col='readerID', 
                   item_col='smart_collapse_field', 
                   weight_col=None, 
                   users_mapping=None, 
                   items_mapping=None):
        if weight_col is None:
            weights = np.ones(len(df), dtype=np.float32)
        else:
            weights = df[weight_col].astype(np.float32)

        interaction_matrix = sp.coo_matrix((
            weights, 
            (
                df[user_col].map(users_mapping.get), 
                df[item_col].map(items_mapping.get)
            )
        ))
        return interaction_matrix
    
    def generate_implicit_recs_mapper(self, model, train_matrix, N, user_mapping, item_inv_mapping):
        def _recs_mapper(user):
            user_id = user_mapping[user]
            recs = model.recommend(user_id, 
                                   train_matrix, 
                                   N=N, 
                                   filter_already_liked_items=True)
            return [item_inv_mapping[item] for item, _ in recs]
        return _recs_mapper
    
    def fit(self, cat, circulaton, readers, n_iter=4):
        cat = self.cat_proc(cat)
        circulaton = self.circulaton_proc(circulaton)
        readers = self.readers_proc(readers)
        
        full_set = pd.merge( 
                        pd.merge(circulaton, cat, how='left', left_on="catalogueRecordID", right_on="id"),
                        readers, how="left", left_on="id", right_on="abis_id")
        full_set = full_set.drop(columns = ['id', 'abis_id'])
        
        now_date = datetime.now()
        last_date = now_date - timedelta(days=self.days)
        most_popular = full_set[(last_date < full_set['startDate']) & (full_set['startDate'] < now_date) ]['smart_collapse_field'].value_counts()[:5]
        
        users_inv_mapping = dict(enumerate(full_set['readerID'].unique()))
        users_mapping = {v: k for k, v in users_inv_mapping.items()}


        items_inv_mapping = dict(enumerate(full_set['smart_collapse_field'].unique()))
        items_mapping = {v: k for k, v in items_inv_mapping.items()}
        
        full_set['readerID'] = full_set['readerID'].astype(int)
        train_matrix = self.get_coo_matrix(full_set, users_mapping=users_mapping, items_mapping=items_mapping).tocsr()
        
        model = BM25Recommender()
        model.fit(train_matrix.T)
        
        top_N = 5
        mapper = self.generate_implicit_recs_mapper(model, train_matrix, top_N, users_mapping, items_inv_mapping)
        
        cold_users_list = full_set['readerID'].value_counts().loc[lambda x : x < n_iter]
        cold_users = pd.DataFrame({'user_id' : cold_users_list.index, 'smart_collapse_field': cold_users_list.values})
        cold_users['smart_collapse_field'] = cold_users['smart_collapse_field'].apply(lambda x: list(most_popular.index))
        recs = pd.DataFrame({
            'readerID': full_set['readerID'].unique()
        })
        recs['itemID'] = recs['readerID'].map(mapper)
        recs = pd.merge(recs, cold_users, how='left', left_on="readerID", right_on="user_id")

        recs['smart_collapse_field'] = recs['smart_collapse_field'].fillna(recs['itemID'])
        recs = recs.drop(columns=['itemID', 'user_id'])
        recs.rename(columns = {'readerID':'user_id'}, inplace = True)
        recs = recs.append({'user_id':0,'smart_collapse_field':list(most_popular.index)}, ignore_index=True)
        
        rec_books_id = pd.DataFrame(recs['smart_collapse_field'].values.tolist(), columns=['book_id_1', 'book_id_2', 'book_id_3', 'book_id_4', 'book_id_5'])
        recs = pd.concat([recs,rec_books_id], axis=1).drop('smart_collapse_field', 1)
        
        key = pd.DataFrame({'smart_collapse_field':full_set['smart_collapse_field'], 'catalogueRecordID':full_set['catalogueRecordID']})
        key = key.drop_duplicates(subset=['smart_collapse_field'])


        recs['book_id_1'] = pd.merge(recs['book_id_1'], key, how='left', left_on="book_id_1", right_on="smart_collapse_field").drop(columns = ['book_id_1', 'smart_collapse_field'])
        recs['book_id_2'] = pd.merge(recs['book_id_2'], key, how='left', left_on="book_id_2", right_on="smart_collapse_field").drop(columns = ['book_id_2', 'smart_collapse_field'])
        recs['book_id_3'] = pd.merge(recs['book_id_3'], key, how='left', left_on="book_id_3", right_on="smart_collapse_field").drop(columns = ['book_id_3', 'smart_collapse_field'])
        recs['book_id_4'] = pd.merge(recs['book_id_4'], key, how='left', left_on="book_id_4", right_on="smart_collapse_field").drop(columns = ['book_id_4', 'smart_collapse_field'])
        recs['book_id_5'] = pd.merge(recs['book_id_5'], key, how='left', left_on="book_id_5", right_on="smart_collapse_field").drop(columns = ['book_id_5', 'smart_collapse_field'])
        
        recs.to_csv('recs.csv',index=False)


cat = pd.read_csv('C:/Users/coolz/cat.csv')
circulaton = pd.read_csv('C:/Users/coolz/circulaton.csv')
readers = pd.read_csv('C:/Users/coolz/readers.csv',index_col=[0])

recs = BooksRecomender()
recs.fit(cat, circulaton, readers)