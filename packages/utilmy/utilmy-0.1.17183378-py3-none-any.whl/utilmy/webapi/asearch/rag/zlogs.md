# kg query benchmarking
   ```bash
   # pyinstrument  engine_kg.py kg_benchmark_queries --dirin ztmp/kg/data/agnews_kg_question.csv --dirout ztmp/kg/data/agnews_kg_benchmark.csv --queries=5
   #ztmp/kg/data/agnews_kg_benchmark.csv
                                             question  ...        dt
   0  What is the relationship between Turner and Fe...  ...  2.298924
   1                What is the capital city of Canada?  ...  1.432849
   2  What is the connection between protein and ami...  ...  2.166291
   3  Who founded the Prediction Unit Helps Forecast...  ...  1.930334
   4  What jurisdiction does the smog-fighting agenc...  ...  1.739533

   [5 rows x 3 columns]
   Average time taken: 1.91 seconds

   _     ._   __/__   _ _  _  _ _/_   Recorded: 20:31:12  Samples:  6916
   /_//_/// /_\ / //_// / //_'/ //     Duration: 19.191    CPU time: 11.769
   /   _/                      v4.6.2

   Program: /home/ankush/workplace/fl_projects/myutil/.venv/bin/pyinstrument engine_kg.py kg_benchmark_queries --dirin ztmp/kg/data/agnews_kg_question.csv --dirout ztmp/kg/data/agnews_kg_benchmark.csv --queries=5

   19.185 <module>  engine_kg.py:1
   ├─ 10.191 Fire  fire/core.py:81
   │     [3 frames hidden]  fire
   │        10.139 _CallAndUpdateTrace  fire/core.py:661
   │        └─ 10.138 kg_benchmark_queries  engine_kg.py:502
   │           ├─ 9.568 kg_db_query  engine_kg.py:438
   │           │  ├─ 9.101 wrapper  llama_index/core/instrumentation/dispatcher.py:258
   │           │  │     [69 frames hidden]  llama_index, tenacity, openai, httpx,...
   │           │  │        4.789 _SSLSocket.read  <built-in>
   │           │  │        3.902 _SSLSocket.read  <built-in>
   │           │  └─ 0.311 KnowledgeGraphIndex.from_documents  llama_index/core/indices/base.py:105
   │           │        [10 frames hidden]  llama_index, tiktoken, tiktoken_ext
   │           └─ 0.382 pd_to_file  utilmy/ppandas.py:585
   │              └─ 0.359 collect  <built-in>
   ├─ 4.273 <module>  spacy/__init__.py:1
   │     [27 frames hidden]  spacy, thinc, torch, <built-in>, conf...
   ├─ 2.399 <module>  llama_index/core/__init__.py:1
   │     [39 frames hidden]  llama_index, openai, llama_index_clie...
   ├─ 1.957 <module>  spacy_component.py:1
   │  └─ 1.892 _LazyModule.__getattr__  transformers/utils/import_utils.py:1494
   │        [46 frames hidden]  transformers, importlib, accelerate, ...
   └─ 0.331 <module>  query.py:1
      └─ 0.320 <module>  dspy/__init__.py:1
            [6 frames hidden]  dspy, dsp, datasets

   To view this report with different options, run:
    pyinstrument --load-prev 2024-05-14T20-31-12 [options]
```







############ 15 May
```
# pykg kg_benchmark_queries --dirin ztmp/kg/data/agnews_kg_questions2.csv --dirout ztmp/kg/data/agnews_kg_benchmark2.csv --queries=20
ztmp/kg/data/agnews_kg_benchmark2.csv
                                             question  ... is_correct
0   Who founded the Prediction Unit that helps for...  ...      False
1   What jurisdiction does the smog-fighting agenc...  ...       True
2   What is an example of an instance of an open l...  ...       True
3                   What product does Sophos produce?  ...       True
4    How is FOAF used in the concept of web-of-trust?  ...       True
5   How does phishing relate to E-mail scam in ter...  ...       True
6    In which country is the Card fraud unit located?  ...       True
7   What type of product or material does STMicroe...  ...       True
8                  Who is the developer of Final Cut?  ...       True
9   Where is the headquarters of Free Record Shop ...  ...      False
10  Which country is the city of Melbourne located...  ...       True
11  How do socialites unite dolphin groups in term...  ...       True
12                 In what instance did the teenage T  ...      False
13  What is Ganymede an instance of within our sol...  ...       True
14  Which space agency operates the Mars Express s...  ...       True

[15 rows x 4 columns]
 Average time taken: 1.97 seconds
 Percentage accuracy: 80.00 %







 
```



#################################################################################
# Llama index graph query logs  using Nebula
```
# pykg kg_db_query --space_name "agnews_kg_relation" --query "Which country is the city of Melbourne located in?"

HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
** Messages: **
user: A question is provided below. Given the question, extract up to 10 keywords from the text. Focus on extracting the keywords that we can use to best lookup answers to the question. Avoid stopwords.
---------------------
Which country is the city of Melbourne located in?
---------------------
Provide keywords in the following comma-separated format: 'KEYWORDS: <keywords>'

**************************************************
** Response: **
assistant: KEYWORDS: country, city, Melbourne, located
**************************************************


Index was not constructed with embeddings, skipping embedding usage...
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
** Messages: **
system: You are an expert Q&A system that is trusted around the world.
Always answer the query using the provided context information, and not prior knowledge.
Some rules to follow:
1. Never directly reference the given context in your answer.
2. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines.
user: Context information is below.
---------------------
kg_schema: {'schema': "Node properties: [{'tag': 'entity', 'properties': [('name', 'string')]}]\nEdge properties: [{'edge': 'relationship', 'properties': [('relationship', 'string')]}]\nRelationships: ['(:entity)-[:relationship]->(:entity)']\n"}

The following are knowledge sequence in max depth 2 in the form of directed graph like:
`subject -[predicate]->, object, <-[predicate_next_hop]-, object_next_hop ...`
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Virgin Blue{name: Virgin Blue}


Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- CANBERRA{name: CANBERRA}

Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Dow Jones{name: Dow Jones}

Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Sons Of Gwalia{name: Sons Of Gwalia}

Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country of citizenship}]- Jana Pittman{name: Jana Pittman}

Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Australia Police to Trap Cyberspace Pedophiles{name: Australia Police to Trap Cyberspace Pedophiles}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: member of sports team}]- Andrew Symonds{name: Andrew Symonds}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country of citizenship}]- Nathan Baggaley{name: Nathan Baggaley}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Sons of Gwalia{name: Sons of Gwalia}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Seven Network Ltd{name: Seven Network Ltd}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- PERTH{name: PERTH}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country of citizenship}]- Rod Eddington{name: Rod Eddington}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Qantas Airways{name: Qantas Airways}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- SYDNEY{name: SYDNEY}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: Which country is the city of Melbourne located in?
Answer: 
**************************************************
** Response: **
assistant: Australia
**************************************************


Australia
```














#########################################################################################

# neo4j triplet insertion
```
# pykg neo_db_insert_triplet_file --dirin ztmp/kg/data/kg_relation.csv --db_name "neo4j" 
 #triples: 1627, total time taken : 8.34 seconds
```

# neo4j + sqlite search
```
pykg neo4j_search --query "Who visited Chechnya?"
#results=16, neo4j query took: 0.01 seconds


query -->Keyword extraction --> Build a cypher query based on those keywords 
         --> Send the cypher query to neo4j
         ---> Get the triplets
         --> Extract the doc_id for each triplet, Score(doc_id)= Frequency of found triplet.
         --> Rank the doc by score
         --> Fetch actual text from the doc_id using SQL, Sqlite.
            --> return results SAME Format than Qdrant, tantiviy Engine
                    Engine 
                    TODO: Official return Format as DataClass.



{"id": "11374492112337794267", "text": "Putin Visits Chechnya Ahead of Election (AP) AP - Russian President Vladimir Putin made an unannounced visit to Chechnya on Sunday, laying flowers at the grave of the war-ravaged region's assassinated president a week before elections for a new leader.", "score": 8}

{"id": "10877731205540525455", "text": "New Chechen Leader Vows Peace, Poll Criticized  GROZNY, Russia (Reuters) - Chechnya's new leader vowed on  Monday to rebuild the shattered region and crush extremists,  after winning an election condemned by rights groups as a  stage-managed show and by Washington as seriously flawed.", "score": 4}

{"id": "12707266912853963705", "text": "Report: Explosion Kills 2 Near Chechyna (AP) AP - An explosion rocked a police building in the restive Dagestan region adjacent to Chechnya on Friday, and initial reports indicated two people were killed, the Interfax news agency said.", "score": 4}



```

# neo4j benchmarking indexing
```
   # pybench bench_v1_create_neo4j_indexes --nrows 20 --nqueries 20
   Model loaded in 6.82 seconds
   ./ztmp/bench/ag_news/kg_triplets/agnews_kg_relation_btest.csv
                     doc_id  ... info_json
   0   10031470251246589555  ...        {}
   1   10031470251246589555  ...        {}
   2   10031470251246589555  ...        {}
   3   13455116945363191971  ...        {}
   4   13380278105912448845  ...        {}
   5   13380278105912448845  ...        {}
   6    9690454179506583527  ...        {}
   7    9690454179506583527  ...        {}
   8    9690454179506583527  ...        {}
   9   13400249423693784533  ...        {}
   10  13400249423693784533  ...        {}
   11  13400249423693784533  ...        {}
   12  13400249423693784533  ...        {}
   13  13400249423693784533  ...        {}
   14  13400249423693784533  ...        {}
   15  10109972785024178695  ...        {}
   16  10572039232808661934  ...        {}
   17  12910890402456928629  ...        {}
   18  12910890402456928629  ...        {}
   19  12910890402456928629  ...        {}
   20  12910890402456928629  ...        {}
   21   9242928626256260421  ...        {}
   22  11247699813360322535  ...        {}
   23  11247699813360322535  ...        {}
   24  11247699813360322535  ...        {}
   25  11247699813360322535  ...        {}
   26  10088096453294362961  ...        {}
   27  10088096453294362961  ...        {}
   28   9276327214733141092  ...        {}
   29  10917529063570538043  ...        {}
   30  11675024175008667160  ...        {}
   31  11675024175008667160  ...        {}
   32  11675024175008667160  ...        {}
   33  11323664445954829208  ...        {}
   34  11323664445954829208  ...        {}
   35  12516784955453086101  ...        {}
   36  11404701768767769131  ...        {}
   37  11404701768767769131  ...        {}
   38  11404701768767769131  ...        {}
   39  11404701768767769131  ...        {}
   40  10480879870885068149  ...        {}
   41  12209054350654622309  ...        {}
   42  12209054350654622309  ...        {}
   43  12209054350654622309  ...        {}
   44  13086739540453328833  ...        {}

   [45 rows x 5 columns]
   Extracted triplets from #20,  dt exec: 20.385884046554565

   ####### Generate questions from triplets ############################
   HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
   HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
   HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
   HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
   ztmp/kg/data/agnews_kg_bquestion.csv
   (20, 5)
   Generated questions from triplets,  dt exec: 10.212386846542358

####### Save records to DBSQL ######################################
Saved #20 records to sqlite,  dt exec: 0.4380199909210205

####### Insert Triplet into neo4j ##################################
 #triplet inserted: 1 / 45,  time : 0.09 seconds
Inserted triplets into neo4j,  dt exec: 0.31346702575683594

```



#######################################################################
# neo4j benchmarking run
   ```


   # pybench bench_v1_neo4j_run --dirout "ztmp/bench" --topk 5 --dataset "ag_news" --dirquery "ztmp/kg/data/agnews_kg_bquestion.csv"

   {'name': 'bench_v1_neo4j_run', 'dirquery': 'ztmp/kg/data/agnews_kg_bquestion.csv', 'dirout2': 'ztmp/bench/ag_news/neo4j/20240531/200902/'}
   ztmp/bench/ag_news/neo4j/20240531/200902//dfmetrics.csv
                        id istop_k        dt
   0   10031470251246589555       1  0.339181
   1   10031470251246589555       1  0.015657
   2   10031470251246589555       1  0.015347
   3   13455116945363191971       0  0.015977
   4   13380278105912448845       1  0.018131
   5   13380278105912448845       1  0.016992
   6    9690454179506583527       1  0.017252
   7    9690454179506583527       1  0.016205
   8    9690454179506583527       1  0.016251
   9   13400249423693784533       1  0.016096
   10  13400249423693784533       1  0.016939
   11  13400249423693784533       1  0.017772
   12  13400249423693784533       0  0.014174
   13  13400249423693784533       0  0.014077
   14  13400249423693784533       1  0.014585
   15  10109972785024178695       1  0.016232
   16  10572039232808661934       1  0.017043
   17  12910890402456928629       0  0.015937
   18  12910890402456928629       1  0.014980
   19  12910890402456928629       1  0.016215
   Avg time per request 0.03225210905075073
   Percentage accuracy 80.0



   ```












#################################################################################
######## Benchmark with 20k text_id
   ```bash
   #### All alias/shorcuts
      source rag/zshorcuts.sh
      export dir0="ztmp/bench/ag_news"


   ########### Steps commands
   ##### Download data from drive
         #1.  download triplet files(*.parquet) from drive into ztmp/bench/ag_news/kg_triplets
               https://drive.google.com/drive/u/0/folders/1QEoR4YGBmoMS9hrZqmNqaqc5A02tllBw 

         # 2. Download corresponding data file(train_120000.parquet) from drive into ztmp/bench/ag_news/aparquet
               https://drive.google.com/drive/u/0/folders/1SOfvpVlIXDXCeMnRmk7B8xzZ3zRyNevl

   
      ##### neo4j  Insert/Indexing
         # 3. add data into sqlite
         pykg dbsql_save_records_to_db --dirin "$dir0/aparquet/*.parquet" --db_path "./ztmp/db/db_sql/datasets.db" --table_name "agnews"


         # 4. insert triplets into neo4j
         pykg neo4j_db_insert_triplet_file --dirin "$dir0/kg_triplets/*.parquet" --db_name "neo4j"


      ###### 5. generate questions from triplets
         pykg kg_generate_questions_from_triplets --dirin "$dir0/kg_triplets/*.parquet" --dirout="$dir0/kg_questions/common_test_questions.parquet" --nrows 100 --batch_size 5




      ###### 6. qdrant dense Insert indexing
         pybench bench_v1_create_dense_indexes --dirbench "$dir0" --dataset "ag_news" 


      ###### 7. qdrant sparse indexing
         pybench bench_v1_create_sparse_indexes --dirbench "$dir0" --dataset "ag_news" 



      ##### runs Benchmark 
         echo -e "\n\n####### Benchmark Results " >> rag/zlogs.md
         echo '```bash ' >> rag/zlogs.md 
   
   
         echo -e '\n########## sparse run' >> rag/zlogs.md 
         pybench bench_v1_sparse_run --dirquery "$dir0/kg_questions/common_test_questions.parquet" --topk 5 >> rag/zlogs.md


         echo -e '\n########## dense run' >> rag/zlogs.md 
         pybench bench_v1_dense_run --dirquery "$dir0/kg_questions/common_test_questions.parquet" --topk 5 >> rag/zlogs.md
         echo '```' >> rag/zlogs.md

         echo -e '\n########## neo4j run' >> rag/zlogs.md 
         pybench bench_v1_neo4j_run --dirquery "$dir0/kg_questions/common_test_questions.parquet" --topk 5 >> rag/zlogs.md


```




 ######  Benchmark Results with 20k text_id
 ```bash


      Comments:
         topk=20  ---> neo4J :  40% --> 60% icnrease
              Idea : some frequent keywords in triplets, go into the results at higher rank.
                   Issues with keywords and triplets matching,
                       --> Neo4J query:  list of doc_id with those triplet containing keyword.
                            keywords -->  fund all triplets where node == kwyrods

                           WITH {keywords} AS keywords
                                       MATCH (entity1)-[rel]-(entity2)
                                       WHERE any(keyword IN keywords WHERE entity1.name CONTAINS keyword 
                                                OR entity2.name CONTAINS keyword 
                                                OR type(rel) CONTAINS keyword)
                                       RETURN entity1, rel, entity2

                     High frequency keywords ---> Higher rank level.

                        TODO: TD-IDF for graph query.... --> reduce frequency frequency



             




      # neo4j run
      # pybench bench_v1_neo4j_run --dirquery ztmp/kg_questions/common_test_questions.parquet --topk 5
      {'name': 'bench_v1_neo4j_run', 'dirquery': 'ztmp/kg_questions/common_test_questions.parquet', 'dirout2': '$dir0/neo4j/20240606/212259/'}
      ztmp/bench/ag_news/neo4j/20240606/212259//dfmetrics.csv
                            id istop_k        dt
      0   14504362844448484081       0  1.780451
      1    5685638213467219607       1  0.157204
      2    5685638213467219607       1  0.141164
      3   13995111925969122086       0  0.106682
      4     638355261286711537       0  0.154347
      ..                   ...     ...       ...
      85  14651180087730350534       0  0.088991
      86  14114327028645677270       1  0.061864
      87  12985424926102133910       0  0.064829
      88   1217961636799403930       1  0.047790
      89   1217961636799403930       1  0.072322

      [90 rows x 3 columns]
      Avg time per request 0.1170915789074368
      Percentage accuracy 40.0



      ## sparse run
      # pybench bench_v1_sparse_run --dirquery ztmp/kg_questions/common_test_questions.parquet --topk 5
      {'name': 'bench_v1_sparse_run', 'server_url': 'http://localhost:6333', 'collection_name': 'hf-ag_news-sparse', 'model_type': 'stransformers', 'model_id': 'naver/efficient-splade-VI-BT-large-query', 'topk': 5, 'dataset': 'ag_news', 'dirquery': 'ztmp/kg_questions/common_test_questions.parquet', 'dirdata2': 'ztmp/bench/norm//ag_news/', 'dirout2': 'ztmp/bench/ag_news/sparse/20240606/212516/'}
      ztmp/bench/ag_news/sparse/20240606/212516//dfmetrics.csv
                            id istop_k        dt
      0   14504362844448484081       1  0.525815
      1    5685638213467219607       1  0.013314
      2    5685638213467219607       1  0.015434
      3   13995111925969122086       1  0.015568
      4     638355261286711537       1  0.014567
      ..                   ...     ...       ...
      85  14651180087730350534       0  0.013839
      86  14114327028645677270       1  0.011379
      87  12985424926102133910       0  0.013664
      88   1217961636799403930       0  0.011786
      89   1217961636799403930       1  0.011545

      [90 rows x 3 columns]
      Avg time per request 0.01991731325785319
      Percentage accuracy 70.0


      ## dense run
      # pybench bench_v1_sparse_run --dirquery ztmp/kg_questions/common_test_questions.parquet --topk 5
      {'name': 'bench_v1_dense_run', 'server_url': 'http://localhost:6333', 'collection_name': 'hf-ag_news-dense', 'model_type': 'stransformers', 'model_id': 'sentence-transformers/all-MiniLM-L6-v2', 'topk': 5, 'dataset': 'ag_news', 'dirquery': 'ztmp/kg_questions/common_test_questions.parquet', 'dirdata2': 'ztmp/bench/norm//ag_news/', 'dirout2': 'ztmp/bench//ag_news/dense/20240606/212617/'}
      ztmp/bench//ag_news/dense/20240606/212617//dfmetrics.csv
                            id istop_k        dt
      0   14504362844448484081       0  0.567876
      1    5685638213467219607       1  0.011049
      2    5685638213467219607       1  0.013134
      3   13995111925969122086       1  0.013515
      4     638355261286711537       1  0.010795
      ..                   ...     ...       ...
      85  14651180087730350534       0  0.009513
      86  14114327028645677270       1  0.011034
      87  12985424926102133910       0  0.010191
      88   1217961636799403930       0  0.009401
      89   1217961636799403930       1  0.010396

      [90 rows x 3 columns]
      Avg time per request 0.016837151845296223
      Percentage accuracy 55.55555555555556









#######################################################################
### rerun topk=20 ; Neo-4J
topk=20 issues, 




{'name': 'bench_v1_neo4j_run', 'dirquery': 'ztmp/bench/ag_news/kg_questions/common_test_questions.parquet', 'dirout2': 'ztmp/bench/ag_news/neo4j/20240608/230004/'}
ztmp/bench/ag_news/neo4j/20240608/230004//dfmetrics.csv
                      id istop_k        dt
0   14504362844448484081       0  0.641470
1    5685638213467219607       1  0.107558
2    5685638213467219607       1  0.099028
3   13995111925969122086       0  0.083485
4     638355261286711537       0  0.238768
..                   ...     ...       ...
85  14651180087730350534       0  0.066895
86  14114327028645677270       1  0.052804
87  12985424926102133910       1  0.051527
88   1217961636799403930       1  0.037039
89   1217961636799403930       1  0.062341

[90 rows x 3 columns]
 Avg time per request 0.11823943191104465
 Percentage accuracy 62.22222222222222






```

