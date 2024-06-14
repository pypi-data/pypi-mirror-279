# -*- coding: utf-8 -*-
"""NER Deberta



   ### Install

     pip install --upgrade utilmy fire python-box
     pip install -q -U bitsandbytes peft accelerate  transformers==4.37.2
     pip install datasets fastembed simsimd seqeval


    ### Dataset Download
        cd asearch
        mkdir -p ./ztmp/
        cd "./ztmp/"
        git clone https://github.com/arita37/data2.git   data
        cd data
        git checkout text

        #### Check Dataset
        cd ../../
        ls ./ztmp/data/ner/ner_geo/


### Usage:
    cd asearch
    export PYTHONPATH="$(pwd)"  ### Need for correct import

    export pyner="python nlp/ner/ner_deberta.py "

    pyner run_train  --dirout ztmp/exp   --cfg config/train.yaml --cfg_name ner_deberta_v1

    pyner run_infer  --dirmodel ztmp/exp  --dirdata



### Usage Legal Doc dataset
    cd asearch 
    
    export pyner="python nlp/ner/ner_deberta.py "
    export dirdata="./ztmp/data/ner/legaldoc"

    pyner data_legalDoc_json_to_parquet  --dir_json $dirdata/raw/NER_VAL.json     --dirout  $dirdata/val/df_val.parquet
    pyner data_legalDoc_json_to_parquet  --dir_json $dirdata/raw/NER_TRAIN.json   --dirout  $dirdata/train/df_train.parquet

    pyner data_legalDoc_create_metadict  --dirin $dirdata     --dir_meta  $dirdata/meta/meta.json


    pyner run_train --dirout ./ztmp/exp/deberta_legal_doc --cfg config/train.yml --cfg_name model_deverta_legal_doc





### Export ONNX model
       python onnx_export.py export --dirin ztmp/exp/20240101/173456/models/pytorch_model.bin  --dirout ztmp/latest/ner_deberta_v1/

       python onnx_export.py run -dirmodel ztmp/latest/ner_deberta_v1  --dirdata ztmp/data/ner/ner_geo/



### Input dataset:
        REQUIRED_SCHEMA_GLOBAL_v1 = [
            ("text_id",  "int64", "global unique ID for   text"),

            ("text", "str", " Core text "),

            ("ner_list", "list", " List of triplets (str_idx_start, str_idx_end, ner_tag) "),
                 str_idx_start : index start of tag inside   String.
                 str_idx_end:    index start of tag inside   String.
            ]



### Extra docs:
        https://colab.research.google.com/drive/1x-LlluSePdD1ekyItadNNQuvlOc65Qpz  



"""

if "Import":
    import json,re, os, pandas as pd, numpy as np,copy
    from dataclasses import dataclass
    from typing import Optional, Union
    from box import Box

    from functools import partial
    import datasets 
    from datasets import Dataset, load_metric
    # If issue dataset: please restart session and run cell again
    from transformers import (
        TrainingArguments,
        Trainer,

        AutoTokenizer,
        AutoModelForTokenClassification,  #### NER Tasks

        ### LLM
    )
    # from transformers.models.qwen2.modeling_qwen2 import
    from transformers.tokenization_utils_base import PreTrainedTokenizerBase, PaddingStrategy

    import spacy, torch

    from utilmy import (date_now, date_now, pd_to_file, log,log2, log_error, pd_read_file, json_save, 
                        config_load, pprint,)
    ### PTYHONPATH="$(pwd)"
    from utils.util_exp import (exp_create_exp_folder, exp_config_override, exp_get_filelist)

    from utilmy import load_function_uri


#########################################################################################
####### Custom dataset : NERGeo data ####################################################

######### Create Split Data, meta.json
def data_NERgeo_create_datasplit():
    """ 
    python nlp/ner/ner_deberta.py data_NERgeo_create_datasplit

    Sample data:

            query	answer	answerfull	answer_fmt
        0	find kindergarten and tech startup in Crack...	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Cracker Barrel Old Cou...
        1	This afternoon, I have an appointment to Mitsu...	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Mitsuwa Marketplace',c...
        2	find train and embassy near by Brooklyn Bri...	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Brooklyn Bridge Park S...
        3	This afternoon, I have an appointment to Nowhe...	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Nowhere',city='New Yor...
        4	This afternoon, I have an appointment to Wawa....	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Wawa',country='US',loc...


    """
    dirout0='./ztmp/out/ner_geo'
    dt = date_now(fmt="%Y%m%d_%H%M%S")
    dirout= os.path.join(dirout0, dt)
    os.makedirs(dirout)


    ##### Load Data #################################################
    #cd ./ztmp/
    #git clone https://github.com/arita37/data2.git   data
    #cd data
    #git checkout text
    dirtrain = "./ztmp/data/ner/ner_geo/df_10000_1521.parquet"
    dirtest  = "./ztmp/data/ner/ner_geo/df_1000.parquet"
    dirout   = "./ztmp/data/ner/ner_geo/"

    df        = pd_read_file(dirtrain)#.sample(2000)
    log(df)
    df_test   = pd_read_file(dirtest)#.head(100)
    log(df_test)

    cols0 = [ "query",	"answer",	"answerfull",	"answer_fmt"]
    assert df[cols0].shape
    assert df_test[cols0].shape

    colsmap= {"query": "text",}
    df      = df.rename(columns= colsmap)
    df_test = df.rename(columns= colsmap)


    #### Data Enhancement ##########################################
    ex= []
    for i in range(200):
        r = df.sample(1).iloc[0].to_dict()
        query = r["text"]
        s = np.random.randint(len(query))
        if np.random.random()>0.5:
            query = query + f', around {s}km. '
        else:
            query = f'around {s} km. ' + query
        r["text"] = query
        ex.append(r)

    # query = query + ", around 8km."
    df  = pd.concat([df, pd.DataFrame(ex)])

    df["ner_list"]      = df.apply(data_NERgeo_fun_prepro_text_predict,      axis=1)
    df_test["ner_list"] = df_test.apply(data_NERgeo_fun_prepro_text_predict, axis=1)
    log( df.head() )
    log( df_test.sample(1).to_dict())


    assert df[["text", "ner_list" ]].shape    
    assert df_test[["text", "ner_list" ]].shape    

   ###### External validation ##################################### 
    nerdata_validate_dataframe(df)
    nerdata_validate_dataframe(df_test)

    pd_to_file(df,      dirout + "/train/df_train.parquet", show=1)
    pd_to_file(df_test, dirout + "/val/df_val.parquet", show=1)


def data_NERgeo_create_label_metadict(dirdata:str="./ztmp/data/ner/ner_geo/"):
    """ 
    python nlp/ner/ner_deberta_v3.py data_NERgeo_create_label_metadict
    """

    log("############# Create Label Mapper")
    # dirdata = dirin.split("raw")[0]    
    nertag_list = ['location', 'city', 'country', 'location_type', 'location_type_exclude']
    nerlabelEngine = NERdata(nertag_list=nertag_list,)
    
    nerlabelEngine.metadict_init()
    nerlabelEngine.metadict_save(dirdata + "/meta/meta.json")



######### Data Loader for Train
def data_NERgeo_load_datasplit(dirin="./ztmp/data/ner/ner_geo"):
    """ 



    """ 
    df = pd_read_file(dirin + "/train")
    log(df)
    assert df[[ "text", "ner_list"  ]].shape
    assert len(df)>1     and df.shape[1]>= 2 


    df_val = pd_read_file(dirin + "/val", )
    log(df_val)
    assert df_val[[ "text", "ner_list"  ]].shape
    assert len(df_val)>1 and df.shape[1]>= 2


    nerdata_validate_dataframe(df, df_val)
    return df, df_val


def data_NERgeo_load_metadict(dirmeta="./ztmp/data/ner/ner_geo/meta/meta.json"):
    nerlabelEngine = NERdata(dirmeta=dirmeta)
    # I2L, L2I, NLABEL_TOTAL, meta_dict =  dlabel.metadict_load(dirmeta=dirmeta)
    #return I2L, L2I, NLABEL_TOTAL, meta_dict 
    
    I2L, L2I, NLABEL_TOTAL, meta_dict =  nerlabelEngine.metadict_load(dirmeta=dirmeta)

    return nerlabelEngine, meta_dict 




########## Custom dataset NERgeo
def data_NERgeo_predict_generate_text_fromtags(dfpred, dirout="./ztmp/metrics/"):
    """  Generate text from TAGS

    """
    if isinstance(dfpred, str):
       dfpred= pd_read_file(dfpred)
    assert dfpred[[ "ner_list", "pred_ner_list"  ]].shape


    def create_answer_from_tag(tag):
      # name=f'location={}'
      tag=sorted(tag, key=lambda x:x['start'])
      final_answer = ""
      list_location_type = []
      list_location_exclude = []
      for t in tag:
        text  =t.get('text') if 'text' in t else t.get("value")

        if t["class"]not in ['location_type', 'location_type_exclude']:
          key = t["class"]
          final_answer += f'{key}={text}\n'

        elif t["class"] == 'location_type':
          list_location_type.append(text)

        elif t["class"] == 'location_type_exclude':
          list_location_exclude.append(text)

      if len(list_location_type):
        text = " and ".join(list_location_type)
        final_answer += f'location_type={text}\n'

      if len(list_location_exclude):
        text = " and ".join(list_location_exclude)
        final_answer += f'list_location_exclude={text}\n'
      return final_answer

    #####  Generate nornalized answer from tag
    dfpred['text_true_str'] = dfpred["ner_list"].apply(create_answer_from_tag)
    dfpred['text_pred_str'] = dfpred["pred_ner_list"].apply(create_answer_from_tag)

    pd_to_file(dfpred, dirout + '/dfpred_text_generated.parquet', show=1)


def data_NERgeo_fun_prepro_text_predict(row):
    """
       # Location, address, city, country, location_type, type_exclude
       # Location_type=\[(.*?)\],location_type_exclude=\[(.*?)\]

    """
    text  = row['answer_fmt']
    query = row["text"]
    # location = re.findall(r"location='(.*?)'", p[0])
    pattern = r"location='(.*?)',"
    matches = re.findall(pattern, text)
    values = []
    if len(matches):
        assert len(matches) == 1, matches
        values.append(
            {
                "class":'location',
                'value': matches[0],
                'start': query.index(matches[0]),
                'end' : query.index(matches[0]) + len(matches[0])
            }
        )

    pattern = r"city='(.*?)',"
    matches = re.findall(pattern, text)
    if len(matches):
        assert len(matches) == 1, matches
        values.append(
            {
                "class":'city',
                'value': matches[0],
                'start': query.index(matches[0]),
                'end' : query.index(matches[0]) + len(matches[0])
            }
        )
    pattern = r"country='(.*?)',"
    matches = re.findall(pattern, text)
    if len(matches):
        assert len(matches) == 1, matches

        values.append(
            {
                "class":'country',
                'value': matches[0],
                'start': query.index(matches[0]),
                'end' : query.index(matches[0]) + len(matches[0])
            }
        )

    pattern = r"location_type=\[(.*?)\]"
    matches = re.findall(pattern, text)
    if len(matches):
        assert len(matches) == 1, matches
        if len(matches[0].strip()):
            for i in matches[0].split(","):
                x = i.strip()
                if x[0] == "'" and x[-1] == "'":
                    x=x[1:-1]
                if x not in query:
                    log(x, query)
                values.append(
                    {
                        "class":'location_type',
                        'value': x,
                        'start': query.index(x),
                        'end' : query.index(x) + len(x)
                    }
                )

    pattern = r"location_type_exclude=\[(.*?)\]"
    matches = re.findall(pattern, text)
    if len(matches):
        assert len(matches) == 1, matches
        if len(matches[0].strip()):
            for i in matches[0].split(","):
                x = i.strip()
                if x[0] == "'" and x[-1] == "'":
                    x=x[1:-1]
                values.append(
                    {
                    "class":'location_type_exclude',
                    'value': x,

                    'start': query.index(x),
                    'end' : query.index(x) + len(x)
                    }
                )
    return values


def data_NERgeo_fun_extract_from_answer_full(row):
    """  
        #             address': '4700 Gilbert Ave',
        #    'city': 'Chicago',
        #    'country': 'United States',
        #    'location_type': 'hot dog stand and viewpoint',
        #    'location_type_exclude': [],
        #     query = row["text"]

    """
    dict_i4 = json.loads(row['answerfull'])['args']
    query = row["text"]
    values =[]
    for key, value in dict_i4.items():
        if key=='place_name':
            key='location'
        if key =='radius' or key=='navigation_style':continue
        if key =='location_type':
            value = value.split("and")
            value = [i.strip() for i in value]
            values.extend([{
                "class":key,
                'value': i,
                'start': query.index(i),
                'end': query.index(i) + len(i)
            } for i in value])
        elif key =='location_type_exclude':
            if isinstance(value, str):
                value = value.split("and")
                value = [i.strip() for i in value]
                values.extend([{
                    "class":key,
                    'value': i,
                    'start': query.index(i),
                    'end': query.index(i) + len(i)
                } for i in value])
            else:
                assert len(value) == 0
        else:
            if value.strip() not in query:
                log(value, 'x', query, 'x', key)
            values.append(
                {
                    "class": key,
                    'value': value.strip(),
                    'start': query.index(value.strip()),
                    'end': query.index(value.strip()) + len(value.strip())
                }
            )
    return values


def data_NERgeo_fun_answer_clean(ss:str):
  ss = ss.replace("search_places(", "")
  return ss



# My laptop
#### I show I share my screen.




######################################################################################################
################## Custom Data : Legal Data ##########################################################
def data_legalDoc_convert_to_gliner_format(cfg=None, dirin=r"ztmp/data/ner/legaldoc/raw/", dirout=r""):
  """ Convert data to json 
  Input : csv or parquet file

  #### evaluation only support fix entity types (but can be easily extended)
  data  = json_load(dirdata)
  eval_data = {
      "entity_types": ['court', 'petitioner', 'respondent', 'judge', 'lawyer', 'date', 'organization', 'geopolitical entity', 'statute', 'provision', 'precedent', 'case_number', 'witness', 'OTHER_PERSON'],
      "samples": data[:10]
  }


  Target Frormat
  [
  {
    "tokenized_text": ["State", "University", "of", "New", "York", "Press", ",", "1997", "."],
    "ner": [ [ 0, 5, "Publisher" ] ]
  }
  ],
  
  """
  def find_indices_in_list(text, start_pos, end_pos):
        words = text.split(" ")
        cumulative_length = 0
        start_index = None
        end_index = None

        for i, word in enumerate(words):
            word_length = len(word) + 1  # Add 1 for space character
            cumulative_length += word_length

            if start_index is None and cumulative_length > start_pos:
                start_index = i

            if cumulative_length > end_pos:
                end_index = i
                break

        return start_index, end_index

  def convert_to_target(data):     
        lowercase_values = {
        'COURT'       : 'court',
        'PETITIONER'  : 'petitioner',
        'RESPONDENT'  : 'respondent',
        'JUDGE'       : 'judge',
        'LAWYER'      : 'lawyer',
        'DATE'        : 'date',
        'ORG'         : 'organization',
        'GPE'         : 'geopolitical entity',
        'STATUTE'     : 'statute',
        'PROVISION'   : 'provision',
        'PRECEDENT'   : 'precedent',
        'CASE_NUMBER' : 'case_number',
        'WITNESS'     : 'witness',
        'OTHER_PERSON': 'OTHER_PERSON'
        }

        targeted_format = []

        for value in data:
            tokenized_text = value['data']['text'].split(" ")      
            ner_tags = []

            for results in value["annotations"][0]['result']:
                ner_list = []
                start, end = find_indices_in_list(value['data']['text'], results['value']['start'],results['value']['end'])
                
                ner_list.append(start)
                ner_list.append(end)
                
                for label in results['value']['labels']:
                    ner_tags.append(ner_list + [lowercase_values[label]])

            targeted_format.append({"tokenized_text" : tokenized_text, "ner":ner_tags})

        return targeted_format

  with open(dirin,'r') as f:
      data = json.load(f)

  data = convert_to_target(data)

  #df["tokenized_text"] = df["text"].apply(lambda x: x.split())
  # 
  #   data= df[[ "tokenized_text", "ner"]].to_json(dirout, orient="records")
  log(str(data)[:100])
  json_save(data, dirout)



def data_legalDoc_json_to_parquet(dir_json, dirout):
    """  LegalDoc to parquet : need to call it 2 times 1 for train, 1 for val
    """
    from utilmy import json_load, os_makedirs, pd_to_file
    data = json_load(dir_json)
    #data_df = convert_from_labelstudio_to_ner_format(data)

    ######### Converter ####################################
    datasets = []
    for sample in data:
        annotations = sample['annotations']
        text        = sample['data']['text']
        

        #### Convert to parquer format
        row = dict(text=text, ner_list=[])
        for annotation in annotations:
            for ddict in annotation['result']:
                row['ner_list'].append(
                    {
                         'start': ddict['value']['start'], 
                         'end'   : ddict['value']['end'], 
                         'class'  : ddict['value']['labels'][0], 
                         "value" : ddict['value']['text']
                    }
                )
        datasets.append(row)

    data_df= pd.DataFrame(datasets)
    pd_to_file(data_df, dirout, show=1)

    log("#######  Extract the NER Tag  ##########################")    
    tag_list = []
    for index, row in data_df.iterrows():
        for tag in row['ner_list']:
            type_of_tag = tag["class"]
            if type_of_tag not in tag_list:
                tag_list.append(type_of_tag)
    tag_list = sorted(tag_list)
    log("tag_list", tag_list)


def data_legalDoc_create_metadict(dirin, dir_meta):
    """ 

       Infos:
         'court',
         'petitioner',
         'respondent',
         'judge',
         'lawyer',
         'date',
         'organization',
         'geopolitical entity',
         'statute',
         'provision',
         'precedent',
         'case_number',
         'witness',
         'OTHER_PERSON'
        ]


    """
    log("#### Create mapping ###############################")
    # nertag_list = ['location', 'city', 'country', 'location_type', 'location_type_exclude']
    nertag_list = [
        'COURT'      ,
        'PETITIONER' ,
        'RESPONDENT' ,
        'JUDGE'      ,
        'LAWYER'     ,
        'DATE'       ,
        'ORG'        ,
        'GPE'        ,
        'STATUTE'    ,
        'PROVISION'  ,
        'PRECEDENT'  ,
        'CASE_NUMBER',
        'WITNESS'    ,
        'OTHER_PERSON'
    ]

    nerlabelEngine = NERdata(nertag_list=nertag_list,)
    nerlabelEngine.metadict_init()
    nerlabelEngine.metadict_save(dir_meta)



def data_legalDoc_load_metadict(dirmeta="./ztmp/data/ner/legaldoc/meta/meta.json"):
    nerlabelEngine = NERdata(dirmeta=dirmeta)
    I2L, L2I, NLABEL_TOTAL, meta_dict =  nerlabelEngine.metadict_load(dirmeta=dirmeta)
    return nerlabelEngine, meta_dict 

####  training loader functions  ####################################
def data_legalDoc_load_datasplit(dirin="./ztmp/data/ner/legaldoc"):
    """ Data Loader for training. """ 
    df = pd_read_file(dirin + "/train", )
    log(df)
    assert df[[ "text", "ner_list"  ]].shape
    assert len(df)>1     and df.shape[1]>= 2 


    df_val = pd_read_file(dirin + "/val", )
    log(df_val)
    assert df_val[[ "text", "ner_list"  ]].shape
    assert len(df_val)>1 and df.shape[1]>= 2

    nerdata_validate_dataframe(df, df_val)
    return df, df_val



    













########################################################################################
##################### Data Validator ###################################################
def test_nerdata():
    # Example usage of NERdata class

    # Define list of nertags
    nertags = ['person', 'organization', 'location']

    # Create an instance of NERdata class
    ner_data = NERdata(nertag_list=nertags)
    log(ner_data.NCLASS, ner_data.N_BOI, ner_data.L2I, ner_data.I2L)
    data = {
        'text': ["John lives in New York.", "Google is based in California."],
        'pred_ner_list': [[0, 6, 6, 6, 6, 2, 5], [4, 6, 6, 6, 6, 5, 6]]
    }
    df = pd.DataFrame(data)

    # Example offset mapping
    offset_mapping = [
        [[(0, 4), (5, 10), (11, 13), (14, 17), (18, 20), (21, 22)]],
        [[(0, 6), (7, 9), (10, 12), (13, 15), (16, 18), (19, 29), (29, 29)]]
    ]
    # Convert predicted classes into span records for NER
    ner_records = ner_data.pd_convert_ner_to_records(df, offset_mapping)
    df['ner_list'] = ner_records
    log((ner_records))

    ner_data.nerdata_validate_dataframe(df)
    ner_data.nerdata_validate_row(ner_records[0])


    # Get class name from class index
    class_name = ner_data.get_class(1)
    log(f"Class name for index 1: {class_name}")

    # Create mapping dictionaries
    log(f"Label to Index mapping: {ner_data.L2I}")
    log(f"Index to Label mapping: {ner_data.I2L}")

    # Convert predictions to span records for single row
    row_df = {
        'text': "John lives in New York.",
        'offset_mapping': [[(0, 4), (5, 10), (11, 13), (14, 17), (18, 21), (22, 24), (25, 28), (29, 33)]]
    }
    pred_list = [0, 1, 2, 0, 0, 0, 3, 0]
    span_record = ner_data.pred2span(pred_list, row_df)
    log(f"Span record: {span_record}")


def data_DEFAULT_load_datasplit(dirin="./ztmp/data/ner/legaldoc"):
    """ Data Loader by DEFAULT for training. """ 
    df = pd_read_file(dirin + "/train", )
    log(df)
    assert df[[ "text", "ner_list"  ]].shape
    assert len(df)>1     and df.shape[1]>= 2 


    df_val = pd_read_file(dirin + "/val", )
    log(df_val)
    assert df_val[[ "text", "ner_list"  ]].shape
    assert len(df_val)>1 and df.shape[1]>= 2

    NERdata().nerdata_validate_dataframe(df, df_val)
    return df, df_val


def data_DEFAULT_load_metadict(dirmeta="./ztmp/data/ner/legaldoc/meta/meta.json"):
    """ Meta Loader by DEFAULT for training. """ 
    nerlabelEngine = NERdata(dirmeta=dirmeta)
    I2L, L2I, NLABEL_TOTAL, meta_dict =  nerlabelEngine.metadict_load(dirmeta=dirmeta)
    return nerlabelEngine, meta_dict 





def nerdata_validate_dataframe(*dflist):
    return NERdata.nerdata_validate_dataframe(*dflist)


def nerdata_validate_row(xdict_record:Union[list, dict], cols_ref=None):
    """Check format of NER records.
    Args:
        x (Union[list, dict]):     NER records to be checked. list of dict or single dict.
        cols_ref (set, optional):  reference set of columns to check against. 
    Returns: bool: True if format of NER records is valid.
    """
    return NERdata.nerdata_validate_row(x=xdict_record, cols_ref=cols_ref)


class NERdata(object):
    def __init__(self,dirmeta=None, nertag_list=None, token_BOI=None):
        """ Utils to normalize NER data for pandas dataframe


            Args:
                nertag_list (list): list of tags. If not provided, default list of tags is used.
                token_BOI (list): list of token BOI values. If not provided, default list of token BOI values is used.
            Info:

                    - text (str): text.
                    - ner_list (list): List of named entity records. Each named entity record is dictionary with following keys:
                        - type (str)            : type of named entity.
                        - predictionstring (str): predicted string for named entity.
                        - start (int)           : start position of named entity.
                        - end (int)             : end position of named entity.
                        - text (str)            : text of named entity.
            Append dix;
                    - default list of tags is: ['location', 'city', 'country', 'location_type', 'location_type_exclude']
        """

        ##### dirmeta ###################################################
        self.dirmeta = dirmeta 


        #### Class #####################################################################
        tags0 = ['location', 'city', 'country', 'location_type', 'location_type_exclude']        
        if nertag_list is None:
            log(f"Using default nertag list inside NERdata.", tags0)
            self.nertag_list = tags0
        else:
            self.nertag_list = nertag_list 


        # self.NCLASS       = len(self.tag) # Gpy40 make mistake here 
        self.NCLASS       = len(self.nertag_list)


        #############################################################################
        #### B-token am I-token, "other" as NA field
        #### We should make sure client provide exactly token_BOI with size 3.
        #### First for begin of words, second for inside and last for other-word.
        token_BOI   = ["B", "I", "Other"]         if token_BOI is None else token_BOI
        if len(token_BOI) != 3:
            log(f"Please use exactly name of token POI with size 3 for Begin, Inside and other word")
            self.token_BOI = ["B", "I", "Other"] 
            
        self.token_BOI = token_BOI
        self.N_BOI  = len(token_BOI) - 1


        #############################################################################
        ### Number of classes for model : B-token, I-token, O-End, + "Other" ####
        self.NCLASS_BOI = self.NCLASS * self.N_BOI + 1

        ### Number of Labels for model : B-token, I-token, O-End, + "Other"  ####
        self.NLABEL_TOTAL = self.NCLASS*2+1 ## due to BOI notation


        ##### Dict mapping ########################################################## 
        L2I, I2L, NCLASS = self.create_map_dict()

        self.L2I    = L2I      ## Label to Index
        self.I2L    = I2L      ## Index to Label
        self.NCLASS = NCLASS   ## NCLASS 


        ##### NER record template for data validation ##############################
        self.ner_dataframe_cols = ['text', 'ner_list']
        self.ner_fields         = ["start", "end", "class", "value"]

        ##### Meta dict load
        self.meta_dict = self.metadict_init()



    def metadict_save(self, dirmeta=None):
        """ Save json mapper to meta.json
        """
        dirout2 = dirmeta if dirmeta is not None else self.dirmeta 
        dirout2 = dirout2 if ".json" in dirout2 else dirout2 + "/meta.json"
        json_save(self.meta_dict, dirout2 )
        log(dirout2)


    def metadict_load(self, dirmeta:str=None):
        """Load mapper from directory containing meta.json 
        Args: dirmeta (str, optional): directory containing meta.json
        Returns: dict containing all mapping.
        """
        from utilmy import glob_glob
        dirmeta = dirmeta if dirmeta is not None else self.dirmeta
        flist = glob_glob(dirmeta)
        flist = [ fi for fi in flist if ".json" in fi.split("/")[-1]  ]
        fi = flist[0]

        if "json" in fi.split("/")[-1].split(".")[-1]:
            with open(fi, 'r') as f:
                meta_dict = json.load(f)

            meta_dict = Box(meta_dict)
            if "meta_dict" in meta_dict.get("data", {}):
                ### Extract meta_dict from config training
                meta_dict = meta_dict["data"]["meta_dict"] 

            self.NLABEL_TOTAL = meta_dict["NLABEL_TOTAL"]
            self.I2L = { int(ii): label   for ii, label in meta_dict["I2L"].items() } ## Force encoding
            self.L2I = { label  : int(ii) for label,ii  in meta_dict["L2I"].items() }
            self.nertag_list = meta_dict['nertag_list']
            self.dirmeta = fi

            self.meta_dict = meta_dict
            return self.I2L, self.L2I, self.NLABEL_TOTAL, meta_dict
        else:
            log(" need meta.json")



    def metadict_init(self,):   
        dd = Box({})
        dd.nertag_list  = self.nertag_list
        dd.NCLASS       = self.NCLASS
        dd.NCLASS_BOI   = self.NCLASS_BOI
        dd.NLABEL_TOTAL = self.NLABEL_TOTAL
        dd.token_BOI    = self.token_BOI
        dd.L2I          = self.L2I
        dd.I2L          = self.I2L
        dd.ner_fields   = self.ner_fields
        dd.ner_dataframe_cols = self.ner_dataframe_cols

        self.meta_dict = dd

    @staticmethod
    def from_meta_dict(meta_dict):
        ner_data_engine = NERdata()
        meta_dict = Box(meta_dict)
        if "meta_dict" in meta_dict.get("data", {}):
            ### Extract meta_dict from config training
            meta_dict = meta_dict["data"]["meta_dict"] 

        ner_data_engine.NLABEL_TOTAL = meta_dict["NLABEL_TOTAL"]
        ner_data_engine.I2L = { int(ii): label   for ii, label in meta_dict["I2L"].items() } ## Force encoding
        ner_data_engine.L2I = { label  : int(ii) for label,ii  in meta_dict["L2I"].items() }
        ner_data_engine.nertag_list = meta_dict['nertag_list']
        ner_data_engine.meta_dict = meta_dict
        return ner_data_engine
    
    def create_metadict(self,):     

        mm ={


        } 

        return mm


    def create_map_dict(self,):        
        NCLASS= self.NCLASS

        begin_of_word  = self.token_BOI[0]
        inside_of_word = self.token_BOI[1]
        other_word     = self.token_BOI[2]
        ### Dict mapping: Label --> Index        
        L2I = {}
        for index, c in enumerate(self.nertag_list):
            L2I[f'{begin_of_word}-{c}'] = index
            L2I[f'{inside_of_word}-{c}'] = index + NCLASS
        L2I[other_word] = NCLASS*2
        L2I['Special'] = -100
        L2I

        ### Dict mapping: Index ---> Label       
        I2L = {}
        for k, v in L2I.items():
            I2L[v] = k
        I2L[-100] = 'Special'

        I2L = dict(I2L)
        log(I2L)

        self.L2I = L2I
        self.I2L = I2L

        return L2I, I2L, NCLASS


    def get_class(self, class_idx:int):
        if class_idx == self.NCLASS_BOI - 1: 
            return self.token_BOI[2]
        else: 
            return self.I2L[class_idx].replace(self.token_BOI[0], "").replace(self.token_BOI[1], "").replace("-", "")


    def pred2span(self, pred_list, row_df, test=False):
        """ Converts list of predicted labels to spans and generates record format for each span.

        Args:
            pred_list (list or numpy.ndarray): list or numpy array of predicted labels.
            row_df (pandas.DataFrame)        : DataFrame containing text and offset_mapping columns.
            test (bool, optional)            : flag indicating whether it is in test mode. Defaults to False.

        Returns:
            dict: dictionary containing text and ner_list fields. ner_list field is list of dictionaries,
                  where each dictionary represents named entity and contains type, value, start, end, and text fields.
        """

        n_tokens = len(row_df['offset_mapping'][0])
        classes  = []
        all_span = []
        log(row_df, pred_list, len(pred_list), n_tokens)
        # Gpt4o make mistake here: pred_list is list or numpy array 
        pred_list = pred_list.tolist() if hasattr(pred_list, "tolist") else pred_list

        for i, c in enumerate(pred_list):
            if i == n_tokens:
                # If we go to end of sentence but for another reason maybe padding, etc so pred_list 
                # often longger than n_tokens
                break
            if i == 0:
                cur_span = list(row_df['offset_mapping'][0][i])
                classes.append(self.get_class(c))
            elif i > 0 and (c-self.NCLASS == pred_list[i-1] or c==pred_list[i-1]):
                # We will go to next-token for current span: B-, I-, I-, I- 
                # Note: index_of_inside_word - NCLASS ===  index_of_begin_word 
                cur_span[1] = row_df['offset_mapping'][0][i][1]
            else:
                all_span.append(cur_span)
                cur_span = list(row_df['offset_mapping'][0][i])
                classes.append(self.get_class(c))
        all_span.append(cur_span)

        text = row_df["text"]
        
        # map token ids to word (whitespace) token ids
        predstrings = []
        for span in all_span:
            span_start  = span[0]
            span_end    = span[1]
            before      = text[:span_start]
            token_start = len(before.split())
            if len(before) == 0:    token_start = 0
            elif before[-1] != ' ': token_start -= 1

            num_tkns   = len(text[span_start:span_end+1].split())
            tkns       = [str(x) for x in range(token_start, token_start+num_tkns)]
            predstring = ' '.join(tkns)
            predstrings.append(predstring)

        #### Generate Record format 
        row   = {  "text": text, "ner_list": []}
        llist = []
        for ner_type, span, predstring in zip(classes, all_span, predstrings):
            if ner_type!=self.token_BOI[2]: # token_BOI[2] == 'Other word'
              e = {
                "class" : ner_type,
                'value' : text[span[0]:span[1]],
                'start': span[0],
                'end'  : span[1],
              }
              llist.append(e)
        row["ner_list"] = llist
    
        return row


    def pd_convert_ner_to_records(self, df_val:pd.DataFrame, offset_mapping: list,
                                col_nerlist="pred_ner_list", col_text="text")->pd.DataFrame:
        """Convert predicted classes into span records for NER.
        Args:
            df_val (pd.DataFrame): DataFrame containing input data. It should have following columns:
                - col_nerlist (str): Column name for predicted classes.
                - col_text (str): Column name for text.
            offset_mapping (list): List of offset mappings.

        Returns:
            list: List of span records for NER. Each span record is dictionary with following keys:
                - text (str): text.
                - ner_list (list): List of named entity records. Each named entity record is dictionary with following keys:
                    - type (str)            : type of named entity.
                    - predictionstring (str): predicted string for named entity.
                    - start (int)           : start position of named entity.
                    - end (int)             : end position of named entity.
                    - text (str)            : text of named entity.

        """
        #### Convert
        pred_class = df_val[col_nerlist].values
        valid      = df_val[[col_text]]
        valid['offset_mapping'] = offset_mapping
        valid = valid.to_dict(orient="records")

        ### pred_class : tuple(start, end, string)
        predicts= [self.pred2span(pred_class[i], valid[i]) for i in range(len(valid))]

        # df_val["ner_list_records"] = [row['ner_list'] for row in predicts]
        
        return [row['ner_list'] for row in predicts]

    @staticmethod
    def nerdata_validate_dataframe(*dflist):

        for df in dflist:
           assert df[["text", "ner_list" ]].shape
           rowset = set(df[ "ner_list"].values[0][0].keys())
           assert rowset.issuperset({"start", "end", "class", "value"}), f"error {rowset}"

    @staticmethod
    def nerdata_validate_row(x:Union[list, dict], cols_ref=None):
        """Check format of NER records.
        Args:
            x (Union[list, dict]):     NER records to be checked. list of dict or single dict.
            cols_ref (set, optional):  reference set of columns to check against. 
        """

        cols_ref = {'start', 'value', "class"} if cols_ref is None else set(cols_ref)

        if isinstance(x, list):
            ner_records = set(x[0].keys())
            assert ner_records.issuperset(cols_ref), f" {ner_records} not in {cols_ref}"

        elif isinstance(x, dict):
            ner_records = set(x.keys())
            assert ner_records.issuperset(cols_ref), f" {ner_records} not in {cols_ref}"

        return True

    @staticmethod
    def nerdata_extract_nertag_from_df(df_or_path):
        df = pd_read_file(df_or_path)
        tag_list = []
        for index, row in df.iterrows():
            for tag in row['ner_list']:
                type_of_tag = tag["class"]
                if type_of_tag not in tag_list:
                    tag_list.append(type_of_tag)
        tag_list = sorted(tag_list)
        log("tag_list", tag_list)
        return tag_list




########################################################################################
##################### Tokenizer helper #################################################
def token_fix_beginnings(labels, n_nerclass):
    """Fix   beginning of list of labels by adjusting   labels based on certain conditions.
    Args:
        labels (list): list of labels.        
    # tokenize and add labels    
    """
    for i in range(1,len(labels)):
        curr_lab = labels[i]
        prev_lab = labels[i-1]
        if curr_lab in range(n_nerclass,n_nerclass*2):
            if prev_lab != curr_lab and prev_lab != curr_lab - n_nerclass:
                labels[i] = curr_lab -n_nerclass
    return labels


def tokenize_and_align_labels(row:dict, tokenizer,  L2I:dict, token_BOI: list):
    """Tokenizes  given examples and aligns  labels.
    Args:
        examples (dict): dictionary containing  examples to be tokenized and labeled.
            - "text" (str):  query string to be tokenized.
            - "ner_list" (list): list of dictionaries representing  entity tags.
                Each dictionary should have  following keys:
                - 'start' (int):  start position of  entity tag.
                - 'end' (int):  end position of  entity tag.
                - "class" (str):  type of  entity tag.

    Returns:
        dict: dictionary containing  tokenized and labeled examples.
            It has  following keys:
            - 'input_ids' (list): list of input ids.
            - 'attention_mask' (list): list of attention masks.
            - 'labels' (list): list of labels.
            - 'token_type_ids' (list, optional): list of token type ids. Only present if 'token_type_ids' is present in  input dictionary.
    """

    o = tokenizer(row["text"],
                  return_offsets_mapping=True,
                  return_overflowing_tokens=True)
    offset_mapping = o["offset_mapping"]
    o["labels"] = []
    NCLASS = (len(L2I) - 1) // 2
    for i in range(len(offset_mapping)):
        labels = [L2I[token_BOI[2]] for i in range(len(o['input_ids'][i]))]
        for tag in row["ner_list"]:
            label_start = tag['start']
            label_end = tag['end']
            label = tag["class"]
            for j in range(len(labels)):
                token_start = offset_mapping[i][j][0]
                token_end = offset_mapping[i][j][1]
                if token_start == label_start:
                    labels[j] = L2I[f'{token_BOI[0]}-{label}']
                if token_start > label_start and token_end <= label_end:
                    labels[j] = L2I[f'{token_BOI[1]}-{label}']

        for k, input_id in enumerate(o['input_ids'][i]):
            if input_id in [0,1,2]:
                labels[k] = -100

        labels = token_fix_beginnings(labels, NCLASS)

        o["labels"].append(labels)

    o['labels']         = o['labels'][0]
    o['input_ids']      = o['input_ids'][0]
    o['attention_mask'] = o['attention_mask'][0]
    if 'token_type_ids' in o:o['token_type_ids'] = o['token_type_ids'][0]
    return o



def data_tokenize_split(df, tokenizer, labelEngine, cc):
    """ 

        {'input_ids': [[1, 8382, 277, 39093, 25603, 31487, 840, 39093, 28368, 59543, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
                      [1, 14046, 271, 5203, 473, 13173, 75204, 270, 6547, 40457, 267, 13946, 5648, 2, 2, 2, 2, 2, 2]],

        'token_type_ids': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 

        'attention_mask': [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]], 

        'offset_mapping': [[(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], 
                           [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]], 

        'labels': [[-100, 8382, 277, 390

    """
    pprint(cc)
    cols         = list(df.columns)
    #max_length   = cc.data.sequence_max_length
    # NLABEL_TOTAL = cc.data.nlabel_total
    # log("nlabel_total: ", NLABEL_TOTAL)

    columns = list(df.columns)

    ds = Dataset.from_pandas(df)
    ds = ds.map(tokenize_and_align_labels, 
                 fn_kwargs={'tokenizer':  tokenizer,
                             "L2I":       labelEngine.L2I, 
                             "token_BOI": labelEngine.token_BOI})

    offset_mapping = ds['offset_mapping']

    ds = ds.remove_columns(['overflow_to_sample_mapping', 'offset_mapping', ] + columns)
    log(ds)
    return ds, offset_mapping



@dataclass
class DataCollatorForNER:
    tokenizer         : PreTrainedTokenizerBase
    padding           : Union[bool, str, PaddingStrategy] = True
    max_length        : Optional[int] = None
    pad_to_multiple_of: Optional[int] = None

    def __call__(self, features):
        label_name        = 'label' if 'label' in features[0].keys() else 'labels'
        labels            = [feature.pop(label_name) for feature in features]
        max_length_labels = max([len(i) for i in labels])
        labels_pad        = np.zeros((len(labels), max_length_labels, )) + -100
        for index in range(len(labels)):
#             log(len(labels[index]), labels[index])
            labels_pad[index, : len(labels[index])] = labels[index]

        batch_size         = len(features)
        flattened_features = features
        batch = self.tokenizer.pad(
            flattened_features,
            padding            = self.padding,
            max_length         = self.max_length,
            pad_to_multiple_of = self.pad_to_multiple_of,
            return_tensors     = 'pt',
        )
        batch['labels'] = torch.from_numpy(labels_pad).long()

        return batch




#################################################################################
######################## Train ##################################################
def run_train(cfg=None, cfg_name="ner_deberta", dirout="./ztmp/exp", istest=1):
    """ 
       python nlp/ner/ner_deberta_new.py run_train  --dirout ztmp/exp   --cfg config/traina/train1.yaml --cfg_name ner_deberta

    """
    log("\n###### User default Params   #######################################")
    if "config":    
        cc = Box()
        cc.model_name='microsoft/deberta-v3-base'

        #### Data name
        cc.dataloader_name = "data_DEFAULT_load_datasplit"     ## Function name for loading
        cc.datamapper_name = "data_DEFAULT_load_metadict"  ## Function name for loading

        cc.n_train = 5  if istest == 1 else 1000000000
        cc.n_val   = 2  if istest == 1 else 1000000000

        #### Train Args
        aa = Box({})
        aa.output_dir                  = f"{dirout}/log_train"
        aa.per_device_train_batch_size = 64
        aa.gradient_accumulation_steps = 1
        aa.optim                       = "adamw_hf"
        aa.save_steps                  = min(100, cc.n_train-1)
        aa.logging_steps               = min(50,  cc.n_train-1)
        aa.learning_rate               = 1e-5
        aa.max_grad_norm               = 2
        aa.max_steps                   = -1
        aa.num_train_epochs            = 1
        aa.warmup_ratio                = 0.2 # 20%  total step warm-up
        # lr_schedulere_type='constant'
        aa.evaluation_strategy = "epoch"
        aa.logging_strategy    = "epoch"
        aa.save_strategy       = "epoch"
        cc.hf_args_train = copy.deepcopy(aa)

        ### HF model
        cc.hf_args_model = {}
        cc.hf_args_model.model_name = cc.model_name


    log("\n###### Config Load  ################################################")
    cfg0 = config_load(cfg)
    cfg0 = cfg0.get(cfg_name, None) if cfg0 is not None else None
    #### Override of cc config by YAML config  ############################### 
    cc = exp_config_override(cc, cfg0, cfg, cfg_name)


    log("\n###### Experiment Folder   #########################################")
    cc = exp_create_exp_folder(task="ner_deberta", dirout=dirout, cc=cc)
    log(cc.dirout) ; del dirout


    log("\n###### Model : Training params ###################################")
    args = TrainingArguments( ** dict(cc.hf_args_train))


    log("\n###### Data Load   #################################################")

    ### data_NERgeo_load_prepro()  , data_NERgeo_load_label_mapper()
    ### Create a python function object from String name
    dataloader_fun = load_function_uri(cc.dataloader_name, globals())
    datamapper_fun = load_function_uri(cc.datamapper_name, globals())

    df, df_val                = dataloader_fun()  ## data_NERgeo_load_datasplit()
    nerlabelEngine, meta_dict = datamapper_fun()  ## NERdata : Label to Index, Index to Label

    nerlabelEngine.nerdata_validate_dataframe(df, df_val)
    # taglist = getattr(cc, 'taglist', ['location', 'city', 'country', 'location_type', 'location_type_exclude'])

    cc.hf_args_model.num_labels = nerlabelEngine.NLABEL_TOTAL  #### NCLASS*2+1 ## due to BOI notation

    df, df_val = df.iloc[:cc.n_train], df_val.iloc[:cc.n_val]

    if "params_data":
        cc.data ={}
        cc.data.cols          = df.columns.tolist()
        cc.data.cols_required = ["text", "ner_list" ]
        cc.data.ner_format    = ["start", "end", "class", "value"]  
        cc.data.cols_remove   = ['overflow_to_sample_mapping', 'offset_mapping', ] + cc.data.cols 
        cc.data.meta_dict     = meta_dict
        
        cc.data.L2I           = meta_dict.L2I     ### label to Index Dict
        cc.data.I2L           = meta_dict.I2L     ### Index to Label Dict
        cc.data.nclass        = meta_dict.NCLASS  ### Number of NER Classes.



    log("\n###### Dataloader setup  ############################################")
    tokenizer = AutoTokenizer.from_pretrained(cc.model_name)
    tokenizer.pad_token = tokenizer.eos_token

    assert set(df[ "ner_list"].values[0][0].keys()) == {"start", "end", "class", "value"}
    dataset_train, _ = data_tokenize_split(df, tokenizer, nerlabelEngine, cc, )  


    assert set(df_val[ "ner_list"].values[0][0].keys()) == {"start", "end", "class", "value"}
    dataset_valid, offset_mapping = data_tokenize_split(df_val, tokenizer, nerlabelEngine, cc,)    
    ### Offset Mapping : Used for validation prediction

    compute_metrics = partial(metrics_ner_callback_train, nerlabelEngine=nerlabelEngine)


    log("\n######### DataCollator #########################################")
    data_collator = DataCollatorForNER(tokenizer)
    log2( data_collator([dataset_train[0], dataset_train[1]]))


    log("\n######### Model : Init #########################################")
    model = AutoModelForTokenClassification.from_pretrained(cc.model_name, 
                               num_labels= cc.hf_args_model.num_labels)

    # for i in model.deberta.parameters():
    #   i.requires_grad=False
    
    log("\n######### Model : Training start ##############################")
    trainer = Trainer(model, args,
        train_dataset  = dataset_train,
        eval_dataset   = dataset_valid,
        tokenizer      = tokenizer,
        data_collator  = data_collator,
        compute_metrics= compute_metrics,
    )

    json_save(cc, f'{cc.dirout}/config.json')
    trainer_output = trainer.train()
    trainer.save_model( f"{cc.dirout}/model")

    cc['metrics_trainer'] = trainer_output.metrics
    json_save(cc, f'{cc.dirout}/config.json',     show=1)
    json_save(cc, f'{cc.dirout}/model/meta.json', show=0)  ### Required when reloading for inference


    log("\n######### Model : Eval Predict  ######################################")
    preds_proba_3d, labels_2d, _ = trainer.predict(dataset_valid)
    
    df_val = pd_predict_format_ner(df_val, preds_proba_3d, labels_2d, 
                               offset_mapping, nerlabelEngine)
    assert df_val[[  "pred_proba", "pred_class", "pred_ner_list"     ]].shape


    log("\n######### Model : Eval Metrics #######################################")   
    assert df_val[[ "text", "ner_list", "pred_ner_list"     ]].shape
    df_val = metrics_ner_calc_full(df_val,)

    pd_to_file(df_val, f'{cc.dirout}/dfval_pred_ner.parquet', show=1)  




def pd_predict_format_ner(df_val:pd.DataFrame, preds_proba_3d:list, labels:list, 
                      offset_mapping: list, nerlabelEngine:NERdata)->pd.DataFrame:
    """ preds_proba: (batch, seq, NCLASS*2+1)    [-3.52225840e-01  5.51

        labels:      (batch,seq)  [[-100   10   10   10   10    3   5    5   10   10 -100 -100]
                                   [-100   10   10   10   10     10   10 -100]]
        pred_class: (batch, seq)  [[ 6  3  6 10 10 10 10 10  4 10 10  4 10  5  4 4]
                                   [ 6  6  6  4 10 10  1 10 10  2  2 10 10 0 10  5]]

        'pred_ner_list_records':
          [{ 'start': 0, 'end': 1, "class": 'ORG', value : "B-ORG"},   ]

            pred_ner_list_records
            List<Struct<{end:Int64, predictionstring:String, start:Int64, text:String, type:String}>>

            accuracy
            Struct<{city:Float64, country:Float64, location:Float64, location_type:Float64, total_acc:Float64}>          

    """    
    pred_class_2d = np.argmax(preds_proba_3d, axis=-1) ### 3d --> 2d by taking Max Proba

    log("pred_proba: ", str(preds_proba_3d)[:50],)
    log("labels: ",     str(labels)[:50]      )
    log("pred_class: ", str(pred_class_2d)[:50] )

    df_val['pred_proba'] = np_3darray_into_2d(preds_proba_3d) 
    df_val['pred_class'] = list(pred_class_2d) ### 2D array into List of List  ## ValueError: Expected 1D array, got an array with shape (2, 25)

    ### Need to convert into (start, end, tag) record format
    df_val['pred_ner_list'] = df_val['pred_class'].apply(lambda x : x)   
    # df_val['preds_labels'] = labels

    df_val['pred_ner_list_records'] = nerlabelEngine.pd_convert_ner_to_records(df_val, offset_mapping)
    return df_val



def np_3darray_into_2d(v3d):
    """ Required to save 3d array in parquet format


    """ 
    shape = v3d.shape
    v2d = np.empty((shape[0], shape[1]), dtype=str)

    for i in range(shape[0]):
        for j in range(shape[1]):
            vstr    = ",".join(map(str, v3d[i,j,:]))
            v2d[i,j]= vstr
    return list(v2d)




################################################################################
########## Run Inference  ######################################################
def run_infer(cfg:str=None, dirmodel="ztmp/models/gliner/small", 
                cfg_name    = "ner_gliner_predict",
                dirdata     = "ztmp/data/text.csv",
                coltext     = "text",
                dirout      = "ztmp/data/ner/predict/",
                multi_label = 0,
                  ):
    """Run prediction using pre-trained  Deberta model.

            ### Usage
            export pyner="python nlp/ner/ner_deberta.py "

            pyner run_infer --dirmodel "./ztmp/exp/20240520/235015/model_final/"  --dirdata "ztmp/data/ner/deberta"  --dirout ztmp/out/ner/deberta/

            pyner run_infer --cfg config/train.yaml     --cfg_name "ner_deberta_infer_v1"


            Output:


        Parameters:
            cfg (dict)    : Configuration dictionary (default is None).
            dirmodel (str): path of pre-trained model 
            dirdata (str) : path of input data 
            coltext (str) : Column name of text
            dirout (str)  : path of output data 


        #log(model.predict("My name is John Doe and I love my car. I bought new car in 2020."))

    """
    cfg0 = config_load(cfg,)
    cfg0 = cfg0.get(cfg_name, None) if isinstance(cfg0, dict) else None 
    if  isinstance( cfg0, dict) : 

        dirmodel = cfg0.get("dirmodel", dirmodel)
        dirdata  = cfg0.get("dirdata",  dirdata)
        dirout   = cfg0.get("dirout",   dirout)
    

    # Model init

    multi_label         = False if multi_label == 0 else True
    model               = AutoModelForTokenClassification.from_pretrained(dirmodel,)
    tokenizer           = AutoTokenizer.from_pretrained(dirmodel)
    tokenizer.pad_token = tokenizer.eos_token
    data_collator       = DataCollatorForNER(tokenizer)
    trainer             = Trainer(model,data_collator  = data_collator,)

    # Meta init
    meta = json.load(open(os.path.join(dirmodel, "meta.json")))
    # because when training we save all meta in the dir of model
    # This is nice, because we can infer without know config, 
    # We need only model directory to infer everything.
    # So when some-one need our model, we only zip folder-model-experiment after training for their.
    nerlabelEngine = NERdata.from_meta_dict(meta['data']['meta_dict']) 
    
    flist = exp_get_filelist(dirdata)
    for ii,fi in enumerate(flist) :
        df = pd_read_file(fi)
        df['text'] = df[coltext]
        if 'ner_list' not in df.columns:
            df['ner_list'] = [{"start": 0, "end": 1, "class": nerlabelEngine.get_class(0), "value": "f"}]
            #Fake label to easy use previous function 
        dataset_valid, offset_mapping = data_tokenize_split(df, tokenizer, nerlabelEngine, cfg0,)
        log(f"\n######### Model : Eval Predict: {fi}  ######################################")
        preds_proba_3d, labels_2d, _ = trainer.predict(dataset_valid)
        
        df_val = pd_predict_format_ner(df, preds_proba_3d, labels_2d, 
                                offset_mapping, nerlabelEngine)
        assert df_val[[  "pred_proba", "pred_class", "pred_ner_list"     ]].shape

        pd_to_file(df, dirout + f"/df_predict_ner_{ii}.parquet", show=1)




################################################################################
########## Run Eval   ##########################################################
def run_eval(cfg:str=None, dirmodel="ztmp/models/gliner/small", 
                cfg_name    = "ner_gliner_predict",
                dirdata     = "ztmp/data/text.csv",
                coltext     = "text",
                dirout      = "ztmp/data/ner/predict/",
                multi_label = 0,
                  ):
    """Run prediction using pre-trained  Deberta model.

            ### Usage
            export pyner="python nlp/ner/ner_deberta.py "

            pyner run_eval --dirmodel "./ztmp/exp/20240520/235015/model_final/"  --dirdata "ztmp/data/ner/deberta"  --dirout ztmp/out/ner/deberta/

            pyner run_eval --cfg config/train.yaml     --cfg_name "ner_deberta_infer_v1"


            Output:


        Parameters:
            cfg (dict)    : Configuration dictionary (default is None).
            dirmodel (str): path of pre-trained model 
            dirdata (str) : path of input data 
            coltext (str) : Column name of text
            dirout (str)  : path of output data 


        #log(model.predict("My name is John Doe and I love my car. I bought new car in 2020."))

    """
    cfg0 = config_load(cfg,)
    cfg0 = cfg0.get(cfg_name, None) if isinstance(cfg0, dict) else None 
    if  isinstance( cfg0, dict) : 

        dirmodel = cfg0.get("dirmodel", dirmodel)
        dirdata  = cfg0.get("dirdata",  dirdata)
        dirout   = cfg0.get("dirout",   dirout)
    

    # Model init

    multi_label         = False if multi_label == 0 else True
    model               = AutoModelForTokenClassification.from_pretrained(dirmodel,)
    tokenizer           = AutoTokenizer.from_pretrained(dirmodel)
    tokenizer.pad_token = tokenizer.eos_token
    data_collator       = DataCollatorForNER(tokenizer)
    trainer             = Trainer(model,data_collator  = data_collator,)

    # Meta init
    meta = json.load(open(os.path.join(dirmodel, "meta.json")))
    # because when training we save all meta in the dir of model
    # This is nice, because we can infer without know config, 
    # We need only model directory to infer everything.
    # So when some-one need our model, we only zip folder-model-experiment after training for their.
    nerlabelEngine = NERdata.from_meta_dict(meta['data']['meta_dict']) 
    
    flist = exp_get_filelist(dirdata)
    for ii,fi in enumerate(flist) :
        df = pd_read_file(fi)
        
        if 'ner_list' not in df.columns:
             log(f"Missing column 'ner_list' for Evaluation in {fi}")       
             continue 
        
        df['text'] = df[coltext]
            
        dataset_valid, offset_mapping = data_tokenize_split(df, tokenizer, nerlabelEngine, cfg0,)
        log(f"\n######### Model : Eval Predict: {fi}  ######################################")
        preds_proba_3d, labels_2d, _ = trainer.predict(dataset_valid)
        
        df_val = pd_predict_format_ner(df, preds_proba_3d, labels_2d, 
                                offset_mapping, nerlabelEngine)
        assert df_val[[  "pred_proba", "pred_class", "pred_ner_list"     ]].shape


        log("\n######### Model : Eval Metrics #######################################")   
        assert df_val[[ "text", "ner_list", "pred_ner_list"     ]].shape
        df_val = metrics_ner_calc_full(df_val,)

        pd_to_file(df_val, dirout + f"/df_eval_ner_{ii}.parquet", show=1)











################################################################################
########## Metrics Helper    ###################################################
def metrics_ner_callback_train(model_out, nerlabelEngine):

    metric = datasets.load_metric("seqeval")
    probas_3d, labels_2d = model_out

    I2L = nerlabelEngine.I2L 
    L2I = nerlabelEngine.L2I

    #### Get prediction from probas 3 dim:
    preds_2d = np.argmax(probas_3d, axis=-1)


    ###### Remove ignored index (special tokens)
    preds_2d_filter = [
        [I2L[p] for (p, l) in zip(pred_1d, label_1d) if l != -100]
        for pred_1d, label_1d in zip(preds_2d, labels_2d)
    ]

    labels_2d_filter = [
        [I2L[l] for (_, l) in zip(pred_1d, label_1d) if l != -100]
        for pred_1d, label_1d in zip(preds_2d, labels_2d)
    ]


    ddict = metric.compute(predictions=preds_2d_filter, references=labels_2d_filter)
    
    return {
        "precision":  ddict["overall_precision"],
        "recall"   :  ddict["overall_recall"],
        "f1"       :  ddict["overall_f1"],
        "accuracy" :  ddict["overall_accuracy"],
    }



def metrics_ner_calc_full(df_val,):
    #### Error due : Need to conver ner_list into  {start, end, tag} format
    log( metrics_ner_accuracy(df_val["ner_list"].iloc[0], df_val['pred_ner_list_records'].iloc[0]) )    
    df_val['accuracy'] = df_val.apply(lambda x: metrics_ner_accuracy(x["ner_list"], 
                                                                     x['pred_ner_list_records']),axis=1 )
    # df_val['f1'] = 
    return df_val



def metrics_ner_accuracy(tags_seq_true:list, tags_seq_pred:list):
    """Calculate   accuracy metric for NER (NER) task.
    Args:
        tags (List[Dict]): List of dict  ground truth tags.
                            contains   'start' index, 'value', and "class" of tag.

        preds (List[Dict]): List of dict predicted tags.
                            contains   'start' index, 'text', and "class" of tag.

    Returns: Dict:   accuracy metric for each tag type

    """
    nerdata_validate_row(tags_seq_true, cols_ref=['start', 'value', "class"])
    nerdata_validate_row(tags_seq_pred, cols_ref=['start', 'value', "class"])

    ### Sort by starting indices
    tags_seq_true = sorted(tags_seq_true, key= lambda x: x['start'])
    tags_seq_pred = sorted(tags_seq_pred, key= lambda x: x['start'])

    acc = {}
    acc_count = {}
    for tag in tags_seq_true:
        value_true = tag['value'] ## NER value 
        type_true  = tag["class"]  ## NER column name

        if type_true not in acc:
            acc[type_true]       = 0
            acc_count[type_true] = 0

        acc_count[type_true] += 1

        for pred in tags_seq_pred:
           if pred["class"] == type_true and pred['value'].strip() == value_true.strip():
              acc[type_true ]+= 1

    total_acc   = sum(acc.values()) / sum(acc_count.values())
    metric_dict = {"accuracy": {tag: v/acc_count[tag] for tag, v in acc.items() } }

    metric_dict['accuracy_total'] = total_acc
    return metric_dict








def metrics_ner_f1score(df_val):
    """ 
           df[[ "ner_list", "pred_ner_list_records" ]]
           
           Global F1 score only  ?? recall, precision
           per row prediction F1 score ?
           
           pip install f1score_ner
           
     
    """
    
    assert df_val[[ "ner_list", "pred_ner_list_records" ]].shape
    dmetrics = {"f1score" : 0.0, "precision": 0.0, "recall": 0.0}
    
    
    
    
    
    return dmetrics
    





################################################################################
########## Eval with Visualization Truth   #####################################
def eval_visualize_tag(dfpred=Union[str, pd.DataFrame], dirmeta:str="./ztmp/NERLegal/meta/meta.json", 
                       ner_colors_dict=None, dirout: str="./ztmp/metrics/ner_visualize", idx_rows="0"):
    """ Visualizes   predicted tags for given dataset of NER tasks.

    python nlp/ner_deberta.py --dfpred "./ztmp/exp/ner_train/dfpred_ner.parquet"    --dirout "./ztmp/exp/ner_train/"

    dfpred[[ "pred_ner_list_records", "text" ]]

    Args:
        dfpred (Union[str, pd.DataFrame]):   path to   CSV file containing   predicted tags or Pandas DataFrame with   predicted tags. Default is None.
        dirout (str):   directory where   output file will be saved. Default is './ztmp/metrics/'.
        ner_colors_dict (dict): dictionary mapping entity types to colors. Default is None.

    """ 
    if isinstance(dfpred, str):
        dfpred = pd_read_file(dfpred)
        
    if 'pred_ner_list_records' not in dfpred.columns:
        # for train.df which missing
        dfpred['pred_ner_list_records'] = dfpred['ner_list']
        
    assert dfpred[[ "text",  "pred_ner_list_records"]].shape
    assert set(dfpred['pred_ner_list_records'].iloc[0].keys()).issuperset( set({"start", "end", "class", "value"}) )        
    log(dfpred.iloc[0])



    ##### meta data
    nerlabelEngine= NERdata(dirmeta= dirmeta)
    log(nerlabelEngine.nertag_list)
    I2L, L2I, NCLASS, meta_dict =  nerlabelEngine.metadict_load(dirmeta=dirmeta)
    if ner_colors_dict is None:
        colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
            "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", 
            "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
        ]
        ner_colors_dict = {key: colors[index % len(colors)] for index, key in enumerate(nerlabelEngine.nertag_list)}

    def row_reformat(row):
        modified_row = {'text': row['text'], 'ner_list': []}
        
        for index, predict_dict in enumerate(row['pred_ner_list_records']):
            #### you need to install Better Align vscode package + shortcut --> auto align
            predict_tag = predict_dict['class']
            start       = predict_dict['start']
            end         = predict_dict['end']
            text_tag    = row['text'][start: end]
            modified_row['ner_list'].append(
                {
                    "class": predict_tag,
                    "start": start,
                    "end"  : end,
                    "text" : text_tag
                }
            )

        return modified_row


    ### Select only specific rows.
    idx_rows = [int(ii) for ii in idx_rows.split(",")] if isinstance(idx_rows, str) else idx_rows

    for ii in idx_rows:
        ddict = row_reformat(dfpred.iloc[ii])
        svg   = ner_text_visualize(ddict,  #
                   ner_class_names=nerlabelEngine.nertag_list,  ### always provided
                   ner_colors_dict=ner_colors_dict)

        # Save the SVG string to a file
        dirout2 = dirout + f"/ner_{ii}.svg"
        with open(dirout2 , "w", encoding="utf-8") as f:
            f.write(svg)




def ner_text_visualize(row:dict,  ner_class_names:list,  title='visualize_model-predicted',
                       ner_colors_dict:list=None,
                       jupyter=False):
    """Visualizes   NER results for given text row.
    Args:
        row (dict)                      : text row to visualize.
        title (str, optional)           : title of   visualization. Defaults to 'visualize_model-predicted'.
        ner_class_names (list, optional)       : list of entity references to include in   visualization. Defaults to None.
        ner_colors_dict (dict, optional): dictionary mapping entity references to colors. Defaults to None.
        jupyter (bool, optional)        : Flag indicating whether   visualization is being rendered in Jupyter Notebook. Defaults to True.

    """
    if ner_colors_dict is None:
        colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
            "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", 
            "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
        ]
        n_colors = len(colors) 
        for ii, key in enumerate(ner_class_names):
            ner_colors_dict[key] = colors[ ii % n_colors   ]
            

    text      = row["text"]
    ner_list  = row["ner_list"]
    ner_spans = [{'start': k['start'], 
                  'end':   k['end'], 
                  'label': k["class"]} for k in ner_list if k["class"] !='Other']

    #### Format to Spacy ########################################
    doc_spacy = {
        "text":  text,
        "ents":  ner_spans,
        "title": title
    }
    options = {"ents": ner_class_names, "colors": ner_colors_dict}
    svg = spacy.displacy.render(doc_spacy, style="ent", options=options, manual=True, jupyter=jupyter)
    return svg 





################################################################################
########## Eval with embedding ground Truth  ###################################
def eval_check_with_embed(df_test, col1='gt_answer_str', col2='predict_answer_str',  dirout="./ztmp/metrics/"):
    """Evaluate   performance of model using embeddings for ground truth and predictions.

    Args:
        df_test (pandas.DataFrame or str):   test dataset to evaluate. If string is provided, it is assumed to be file path and   dataset is loaded from that file.
        col1 (str, optional):   name of   column containing   ground truth answers. Defaults to 'gt_answer_str'.
        col2 (str, optional):   name of   column containing   predicted answers. Defaults to 'predict_answer_str'.
        dirout (str, optional):   directory to save   evaluation metrics. Defaults to './ztmp/metrics/'.
    """

    df_test = pd_add_embed(df_test, col1, col2, add_similarity=1, colsim ='sim')

    log( df_test['sim'].describe())
    log( df_test[[col1, col2]].sample(1))

    pd_to_file( df_test[["text", col1, col2, 'sim']],
                f'{dirout}/predict_sim_cosine.parquet') 

    cc = Box({})
    cc['metric_sim'] = df_test['sim'].describe().to_dict()
    json_save(cc, f"{dirout}/metrics_sim_cosine.json")


def qdrant_embed(wordlist, model_name="BAAI/bge-small-en-v1.5", size=128, model=None):
    """ pip install fastembed

    Docs:

         BAAI/bge-small-en-v1.5 384   0.13
         BAAI/bge-base-en       768   0.14
         sentence-transformers/all-MiniLM-L6-v2   0.09

        ll= list( qdrant_embed(['ik', 'ok']))


        ### https://qdrant.github.io/fastembed/examples/Supported_Models/
        from fastembed import TextEmbedding
        import pandas as pd
        pd.set_option("display.max_colwidth", None)
        pd.DataFrame(TextEmbedding.list_supported_models())


    """
    from fastembed.embedding import FlagEmbedding as Embedding

    if model is None:
       model = Embedding(model_name= model_name, max_length= 512)

    vectorlist = model.embed(wordlist)
    return np.array([i for i in vectorlist])


def sim_cosinus_fast(v1, v2)-> float :
   ### %timeit sim_cosinus_fast(ll[0], ll[1])  0.3 microSec
   import simsimd
   dist = simsimd.cosine(v1, v2)
   return dist


def sim_cosinus_fast_list(v1, v2) :
   ### %timeit sim_cosinus_fast(ll[0], ll[1])  0.3 microSec
   import simsimd
   vdist = []
   for x1,x2 in zip(v1, v2):
       dist = simsimd.cosine(x1, x2)
       vdist.append(dist)
   return vdist


def pd_add_embed(df, col1:str="col_text1", col2:str="col_text2", size_embed=128, add_similarity=1, colsim=None):
    """
    df=  pd_add_embed(df, 'answer', 'answerfull', add_similarity=1)
    df['sim_answer_answerfull'].head(1)


    """
    v1 = qdrant_embed(df[col1].values)
    #     return v1
    df[col1 + "_vec"] = list(v1)

    #    if col2 in df.columns:
    v1 = qdrant_embed(df[col2].values)
    df[col2 + "_vec"] = list(v1)

    if add_similarity>0:
      colsim2 = colsim if colsim is not None else f'sim_{col1}_{col2}'
      vdist   = sim_cosinus_fast_list(df[col1 + "_vec"].values, df[col2 + "_vec"].values)
      df[ colsim2 ] = vdist
    return df


def  pd_add_sim_fuzzy_score(df:pd.DataFrame, col1='answer_fmt', col2='answer_pred_clean'):
  # pip install rapidfuzz
  from rapidfuzz import fuzz
  df['dist2'] = df[[col1, col2]].apply(lambda x: fuzz.ratio( x[col1], x[col2]), axis=1)
  return df




################################################################################
########## Text Generator  #####################################################

def run_text_generator_from_tag(dirin, dirout):
    #### Generate answer/text from TAG
    pass 







################################################################################
########## utils  ##############################################################
def pd_predict_convert_ner_to_records(df_val:pd.DataFrame, offset_mapping: list,
                                       col_nerlist="pred_ner_list", col_text="text", cc=None)->pd.DataFrame:
    """Convert predicted classes into span records for NER.

    Args:
        df_val (pd.DataFrame): DataFrame containing input data. It should have following columns:
            - col_nerlist (str): Column name for predicted classes.
            - col_text (str): Column name for text.
        offset_mapping (list): List of offset mappings.

    Returns:
        list: List of span records for NER. Each span record is dictionary with following keys:
            - text (str): text.
            - ner_list (list): List of named entity records. Each named entity record is dictionary with following keys:
                - type (str)            : type of named entity.
                - predictionstring (str): predicted string for named entity.
                - start (int)           : start position of named entity.
                - end (int)             : end position of named entity.
                - text (str)            : text of named entity.

    """
    # log(df_val)
    # assert df_val[[ "text", "input_ids", "offset_mapping", "pred_ner_list"  ]]

    I2L    = cc.data.meta_dict.I2l
    NCLASS =  cc.data.meta_dict.NCLASS

    def get_class(c):
        if c == NCLASS*2: return 'Other'
        else: return I2L[c][2:]

    def pred2span(pred_list, df_row, viz=False, test=False):
        #     example_id = example['id']
        n_tokens = len(df_row['offset_mapping'][0])
        #     log(n_tokens, len(example['offset_mapping']))
        classes = []
        all_span = []
        for i, c in enumerate(pred_list.tolist()):
            if i == n_tokens-1:
                break
            if i == 0:
                cur_span = df_row['offset_mapping'][0][i]
                classes.append(get_class(c))
            elif i > 0 and (c == pred_list[i-1] or (c-NCLASS) == pred_list[i-1]):
                cur_span[1] = df_row['offset_mapping'][0][i][1]
            else:
                all_span.append(cur_span)
                cur_span = df_row['offset_mapping'][0][i]
                classes.append(get_class(c))
        all_span.append(cur_span)

        text = df_row["text"]
        
        # map token ids to word (whitespace) token ids
        predstrings = []
        for span in all_span:
            span_start  = span[0]
            span_end    = span[1]
            before      = text[:span_start]
            token_start = len(before.split())
            if len(before) == 0:    token_start = 0
            elif before[-1] != ' ': token_start -= 1

            num_tkns   = len(text[span_start:span_end+1].split())
            tkns       = [str(x) for x in range(token_start, token_start+num_tkns)]
            predstring = ' '.join(tkns)
            predstrings.append(predstring)

        #### Generate Record format 
        row = {  "text": text, "ner_list": []}
        es = []
        for ner_type, span, predstring in zip(classes, all_span, predstrings):
            if ner_type!='Other':
              e = {
                "class" : ner_type,
                'value': predstring,
                'start': span[0],
                'end'  : span[1],
                'text' : text[span[0]:span[1]]
              }
              es.append(e)
        row["ner_list"] = es
    
        return row


    #### Convert
    pred_class = df_val[col_nerlist].values
    valid      = df_val[[col_text]]
    valid['offset_mapping'] = offset_mapping
    valid = valid.to_dict(orient="records")

    ### pred_class : tuple(start, end, string)
    predicts= [pred2span(pred_class[i], valid[i]) for i in range(len(valid))]

    return [row['ner_list'] for row in predicts]


    #pd_to_file( predicts, dirout + '/predict_ner_visualize.parquet' )
    # pred = pd.read_csv("nguyen/20240215_171305/predict.csv")
    # pred
    # pred = pred[["text", "ner_list"]]
    # eval(pred.ner_tag.iloc[0])
    # pred["ner_list"] = pred["ner_list"].apply(eval)




def init_googledrive(shortcut="phi2"):
    import os
    from google.colab import drive
    drive.mount('/content/drive')
    os.chdir(f"/content/drive/MyDrive/{shortcut}/")
    # ! ls .
    #! pwd
    #! ls ./traindata/
    #ls










###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()






""" 
### nerGEO dataset
    ###### Config Load   #############################################
    Config: Loading  config/train.yaml
    Config: Cannot read file config/train.yaml [Errno 2] No such file or directory: 'config/train.yaml'
    Config: Using default config
    {'field1': 'test', 'field2': {'version': '1.0'}}
    ###### User Params   #############################################
    {'model_name': 'microsoft/deberta-v3-base', 'dataloader_name': 'data_NERgeo_load_prepro', 'datamapper_name': 'data_NERgeo_create_label_mapper', 'n_train': 5, 'n_val': 2, 'hf_args_train': {'output_dir': 'ztmp/exp/log_train', 'per_device_train_batch_size': 64, 'gradient_accumulation_steps': 1, 'optim': 'adamw_hf', 'save_steps': 4, 'logging_steps': 4, 'learning_rate': 1e-05, 'max_grad_norm': 2, 'max_steps': -1, 'num_train_epochs': 1, 'warmup_ratio': 0.2, 'evaluation_strategy': 'epoch', 'logging_strategy': 'epoch', 'save_strategy': 'epoch'}, 'hf_args_model': {'model_name': 'microsoft/deberta-v3-base', 'num_labels': 1}, 'cfg': 'config/train.yaml', 'cfg_name': 'ner_deberta_v1'}
    ###### Experiment Folder   #######################################
    ztmp/exp/20240524/014651-ner_deberta-5
    ###### Model : Training params ##############################
    ###### Data Load   #############################################
                                                      answer  ...                                              query
    0      b'{"name":"search_places","args":{"place_name"...  ...  find  kindergarten and tech startup  in  Crack...
    1      b'{"name":"search_places","args":{"place_name"...  ...  This afternoon, I have an appointment to Mitsu...
    2      b'{"name":"search_places","args":{"place_name"...  ...  find  train and embassy  near by  Brooklyn Bri...
    3      b'{"name":"search_places","args":{"place_name"...  ...  This afternoon, I have an appointment to Nowhe...
    4      b'{"name":"search_places","args":{"place_name"...  ...  This afternoon, I have an appointment to Wawa....
    ...                                                  ...  ...                                                ...
    9997   b'{"name":"search_places","args":{"place_name"...  ...  Next week, I am going to US. show me  fashion ...
    9998   b'{"name":"search_places","args":{"place_name"...  ...  Tomorrow, I am travelling to Fort Lauderdale. ...
    9999   b'{"name":"search_places","args":{"place_name"...  ...   I need to visit Naples. search  portuguese re...
    10000  b'{"name":"search_places","args":{"place_name"...  ...  list some   indoor cycling and speakeasy  arou...
    10001  b'{"name":"search_places","args":{"place_name"...  ...  find  fabric store and driving range  in  Hors...

    [10002 rows x 4 columns]
                                                     answer  ...                                              query
    0     b'{"name":"search_places","args":{"place_name"...  ...  This afternoon, I have an appointment to Barde...
    1     b'{"name":"search_places","args":{"place_name"...  ...  provide  college and alternative healthcare  n...
    2     b'{"name":"search_places","args":{"place_name"...  ...  list some   mountain and public artwork  near ...
    3     b'{"name":"search_places","args":{"place_name"...  ...  Next week, I am going to US. what are   te...
    4     b'{"name":"search_places","args":{"place_name"...  ...   I need to visit Naples. give me  rest area an...
    ...                                                 ...  ...                                                ...
    996   b'{"name":"search_places","args":{"place_name"...  ...  provide  miniature golf and field  at  Apni Ma...
    997   b'{"name":"search_places","args":{"place_name"...  ...  Next week, I am going to US. what are   ba...
    998   b'{"name":"search_places","args":{"place_name"...  ...   I need to visit Fort Snelling.  provide  medi...
    999   b'{"name":"search_places","args":{"place_name"...  ...  Tomorrow, I am travelling to Houston.  find  t...
    1000  b'{"name":"search_places","args":{"place_name"...  ...  Tomorrow, I am travelling to Madison. provide ...

    [1001 rows x 4 columns]
                                                  answer  ...                                           ner_list
    0  b'{"name":"search_places","args":{"place_name"...  ...  [{"class": 'location', 'value': 'Cracker Barrel...
    1  b'{"name":"search_places","args":{"place_name"...  ...  [{"class": 'location', 'value': 'Mitsuwa Market...
    2  b'{"name":"search_places","args":{"place_name"...  ...  [{"class": 'location', 'value': 'Brooklyn Bridg...
    3  b'{"name":"search_places","args":{"place_name"...  ...  [{"class": 'location', 'value': 'Nowhere', 'sta...
    4  b'{"name":"search_places","args":{"place_name"...  ...  [{"class": 'location', 'value': 'Wawa', 'start'...

    [5 rows x 5 columns]
    {'answer': {9392: b'{"name":"search_places","args":{"place_name":"","address":"","city":"Missoula","country":"US","location_type":"tree and photographer","location_type_exclude":[],"radius":"","navigation_style":""}}'}, 'answer_fmt': {9392: "search_places(city='Missoula',country='US',location_type=['tree', 'photographer'],location_type_exclude=[])"}, 'answerfull': {9392: b'{"name":"search_places","args":{"place_name":"Washington Grizzly Stadium","address":"32 Campus Dr","city":"Missoula","country":"US","location_type":"tree and photographer","location_type_exclude":[],"radius":2,"navigation_style":"driving"}}'}, 'text': {9392: 'Next week, I am going to US. give me  tree and photographer  near by  Missoula.'}, 'ner_list': {9392: [{"class": 'city', 'value': 'Missoula', 'start': 70, 'end': 78}, {"class": 'country', 'value': 'US', 'start': 25, 'end': 27}, {"class": 'location_type', 'value': 'tree', 'start': 38, 'end': 42}, {"class": 'location_type', 'value': 'photographer', 'start': 47, 'end': 59}]}}
    {0: 'B-location', 5: 'I-location', 1: 'B-city', 6: 'I-city', 2: 'B-country', 7: 'I-country', 3: 'B-location_type', 8: 'I-location_type', 4: 'B-location_type_exclude', 9: 'I-location_type_exclude', 10: 'Other', -100: 'Special'}
    ###### Dataloader setup  ############################################
    Map: 100%|█████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 353.81 examples/s]
    Map: 100%|█████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 229.00 examples/s]
    You're using DebertaV2TokenizerFast tokenizer. Please note that with fast tokenizer, using `__call__` method is faster than using method to encode text followed by call to `pad` method to get padded encoding.
    {'input_ids': [1, 433, 14047, 263, 3539, 7647, 267, 56693, 24057, 2951, 4631, 4089, 80872, 260, 2], 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'labels': [-100, 10, 10, 10, 10, 3, 10, 10, 0, 5, 5, 5, 10, 10, -100]}
    {'__index_level_0__': tensor([0, 1]), 'input_ids': tensor([[    1,   433, 14047,   263,  3539,  7647,   267, 56693, 24057,  2951,
              4631,  4089, 80872,   260,     2,     2,     2,     2,     2,     2,
                 2,     2,     2,     2,     2],
            [    1,   329,  2438,   261,   273,   286,   299,  3198,   264, 63526,
              6608, 21289,   260,   350, 26026,   263,  4526,   441, 63526,  6608,
             21289,   267,   846,   260,     2]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1]]), 'labels': tensor([[-100,   10,   10,   10,   10,    3,   10,   10,    0,    5,    5,    5,
               10,   10, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100,
             -100],
            [-100,   10,   10,   10,   10,   10,   10,   10,   10,   10,    0,    5,
               10,   10,   10,   10,   10,   10,   10,   10,   10,   10,   10,   10,
             -100]])}
    ######### Model : Init #########################################
    Some weights of DebertaV2ForTokenClassification were not initialized from model checkpoint at microsoft/deberta-v3-base and are newly initialized: ['classifier.bias', 'classifier.weight']
    You should probably TRAIN this model on down-stream task to be able to use it for predictions and inference.
    ######### Model : Training start ##############################
    {'loss': 2.7838, 'grad_norm': 27.501415252685547, 'learning_rate': 0.0, 'epoch': 1.0}                        
    {'eval_loss': 2.8043107986450195, 'eval_precision': 0.0, 'eval_recall': 0.0, 'eval_f1': 0.0, 'eval_accuracy': 0.0, 'eval_runtime': 1.2255, 'eval_samples_per_second': 1.632, 'eval_steps_per_second': 0.816, 'epoch': 1.0}
    100%|██████████████████████████████████████████████████████████████████████████| 1/1 [00:04<00:00,  2.99s/it^{'train_runtime': 11.2399, 'train_samples_per_second': 0.445, 'train_steps_per_second': 0.089, 'train_loss': 2.7838191986083984, 'epoch': 1.0}
    100%|██████████████████████████████████████████████████████████████████████████| 1/1 [00:11<00:00, 11.26s/it]
    {'model_name': 'microsoft/deberta-v3-base', 'dataloader_name': 'data_NERgeo_load_prepro', 'datamapper_name': 'data_NERgeo_create_label_mapper', 'n_train': 5, 'n_val': 2, 'hf_args_train': {'output_dir': 'ztmp/exp/log_train', 'per_device_train_batch_size': 64, 'gradient_accumulation_steps': 1, 'optim': 'adamw_hf', 'save_steps': 4, 'logging_steps': 4, 'learning_rate': 1e-05, 'max_grad_norm': 2, 'max_steps': -1, 'num_train_epochs': 1, 'warmup_ratio': 0.2, 'evaluation_strategy': 'epoch', 'logging_strategy': 'epoch', 'save_strategy': 'epoch'}, 'hf_args_model': {'model_name': 'microsoft/deberta-v3-base', 'num_labels': 11}, 'cfg': 'config/train.yaml', 'cfg_name': 'ner_deberta_v1', 'dirout': 'ztmp/exp/20240524/014651-ner_deberta-5', 'data': {'cols': ['answer', 'answer_fmt', 'answerfull', 'text', 'ner_list'], 'cols_required': ['text', 'ner_list'], 'ner_format': ['start', 'end', "class", 'value'], 'cols_remove': ['overflow_to_sample_mapping', 'offset_mapping', 'answer', 'answer_fmt', 'answerfull', 'text', 'ner_list'], 'L2I': {'B-location': 0, 'I-location': 5, 'B-city': 1, 'I-city': 6, 'B-country': 2, 'I-country': 7, 'B-location_type': 3, 'I-location_type': 8, 'B-location_type_exclude': 4, 'I-location_type_exclude': 9, 'Other': 10, 'Special': -100}, 'I2L': {0: 'B-location', 5: 'I-location', 1: 'B-city', 6: 'I-city', 2: 'B-country', 7: 'I-country', 3: 'B-location_type', 8: 'I-location_type', 4: 'B-location_type_exclude', 9: 'I-location_type_exclude', 10: 'Other', -100: 'Special'}, 'nclass': 5}, 'metrics_trainer': {'train_runtime': 11.2399, 'train_samples_per_second': 0.445, 'train_steps_per_second': 0.089, 'total_flos': 63799496250.0, 'train_loss': 2.7838191986083984, 'epoch': 1.0}}
    <_io.TextIOWrapper name='ztmp/exp/20240524/014651-ner_deberta-5/config.json' mode='w' encoding='UTF-8'>
    ######### Model : Eval Predict  ######################################
    100%|██████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.43s/it]
    pred_proba:  [[[ 0.25330016 -0.47247496 -0.08278726 -0.06999959
    labels:  [[-100   10   10   10   10    3   10   10    0    
    pred_class:  [[ 0  2  0  2  2  0  2  2  1  2  2  2  9  2  0 10 
    {'text': 'find  kindergarten and tech startup  in  Cracker Barrel Old Country Store Rialto.', 'offset_mapping': [[[0, 0], [0, 4], [5, 18], [18, 22], [22, 27], [27, 35], [36, 39], [40, 48], [48, 55], [55, 59], [59, 67], [67, 73], [73, 80], [80, 81], [0, 0]]]} [ 0  2  0  2  2  0  2  2  1  2  2  2  9  2  0 10 10 10 10 10 10 10 10 10
     10] 25 15
    {'text': 'This afternoon, I have an appointment to Mitsuwa Marketplace. get  deli and resort  around  Mitsuwa Marketplace in US.', 'offset_mapping': [[[0, 0], [0, 4], [4, 14], [14, 15], [15, 17], [17, 22], [22, 25], [25, 37], [37, 40], [40, 46], [46, 48], [48, 60], [60, 61], [61, 65], [66, 71], [71, 75], [75, 82], [83, 90], [91, 97], [97, 99], [99, 111], [111, 114], [114, 117], [117, 118], [0, 0]]]} [0 0 2 0 5 2 0 2 9 2 2 2 3 0 0 0 1 2 2 2 2 8 9 0 0] 25 25
    ######### Model : Eval Metrics #######################################
    {'accuracy': {'location_type': 0.0, 'location': 0.0, 'city': 0.0}, 'accuracy_total': 0.0}
    ztmp/exp/20240524/014651-ner_deberta-5/dfval_pred_ner.parquet
                                                  answer  ...                                           accuracy
    0  b'{"name":"search_places","args":{"place_name"...  ...  {'accuracy': {'location_type': 0.0, 'location'...
    1  b'{"name":"search_places","args":{"place_name"...  ...  {'accuracy': {'location': 0.0, 'location_type'...

    [2 rows x 10 columns]




### LEGAL DOC

           python3 nlp/ner/ner_deberta_new.py run_train --dirout ztmp/exp_deberta_legal_doc --cfg config/train.yml --cfg_name model_deverta_legal_doc

            ###### User default Params   #######################################

            ###### Config Load  ################################################
            Config: Loading  config/train.yml
            ###### Overide by config model_deverta_legal_doc ####################
            {'model_name': 'microsoft/deberta-v3-base', 'dataloader_name': 'data_legalDoc_load_datasplit', 'datamapper_name': 'data_legalDoc_load_metadict', 'n_train': 5, 'n_val': 2, 'hf_args_train': {'output_dir': 'ztmp/exp_deberta_legal_doc/log_train', 'per_device_train_batch_size': 64, 'gradient_accumulation_steps': 1, 'optim': 'adamw_hf', 'save_steps': 4, 'logging_steps': 4, 'learning_rate': 1e-05, 'max_grad_norm': 2, 'max_steps': -1, 'num_train_epochs': 1, 'warmup_ratio': 0.2, 'evaluation_strategy': 'epoch', 'logging_strategy': 'epoch', 'save_strategy': 'epoch'}, 'hf_args_model': {'model_name': 'microsoft/deberta-v3-base'}, 'cfg': 'config/train.yml', 'cfg_name': 'model_deverta_legal_doc', 'model_path': 'model_deberta', 'model_type': 'deberta', 'dirin': 'ztmp/data/ner/legaldoc/'}

            ###### Experiment Folder   #########################################
            ztmp/exp_deberta_legal_doc/20240602/110950-ner_deberta-5

            ###### Model : Training params ###################################

            ###### Data Load   #################################################
                                                        ner_list                                               text
            0     [{'class': 'ORG', 'end': 103, 'start': 90, 'va...  \n\n(7) On specific query by the Bench about a...
            1     [{'class': 'OTHER_PERSON', 'end': 30, 'start':...  He was also asked whether Agya <span class="hi...
            2     [{'class': 'WITNESS', 'end': 25, 'start': 13, ...   \n5.2 CW3 Mr Vijay Mishra , Deputy Manager, H...
            3                                                    []  You are hereby asked not to carry out any cons...
            4     [{'class': 'OTHER_PERSON', 'end': 43, 'start':...  The pillion rider T.V. Satyanarayana Murthy al...
            ...                                                 ...                                                ...
            9430  [{'class': 'STATUTE', 'end': 226, 'start': 202...  It is prayed in the application that the suit ...
            9431  [{'class': 'OTHER_PERSON', 'end': 35, 'start':...  In the first instance, Mr.A.D.Desai contended ...
            9432  [{'class': 'JUDGE', 'end': 5, 'start': 0, 'val...  Sikri, J. (as he then was), speaking for the m...
            9433  [{'class': 'JUDGE', 'end': 17, 'start': 1, 'va...  (RAJENDRA MAHAJAN) JUDGE AKM M.Cr.C. No. 8763/...
            9434  [{'class': 'DATE', 'end': 153, 'start': 144, '...  In the cross-examination, PW.12 has admitted t...

            [9435 rows x 2 columns]
                                                        ner_list                                               text
            0   [{'class': 'ORG', 'end': 103, 'start': 90, 'va...  \n\n(7) On specific query by the Bench about a...
            1   [{'class': 'OTHER_PERSON', 'end': 30, 'start':...  He was also asked whether Agya <span class="hi...
            2   [{'class': 'WITNESS', 'end': 25, 'start': 13, ...   \n5.2 CW3 Mr Vijay Mishra , Deputy Manager, H...
            3                                                  []  You are hereby asked not to carry out any cons...
            4   [{'class': 'OTHER_PERSON', 'end': 43, 'start':...  The pillion rider T.V. Satyanarayana Murthy al...
            5   [{'class': 'STATUTE', 'end': 123, 'start': 119...  , if the argument of the learned counsel for t...
            6                                                  []  After all the steps at the stage of investigat...
            7   [{'class': 'WITNESS', 'end': 18, 'start': 6, '...  PW--2 Chandregowda is the younger brother of b...
            8                                                  []  What is the main offence in the charges involv...
            9   [{'class': 'DATE', 'end': 39, 'start': 30, 'va...  He had prepared G.D. No. 7 on 19.8.1998 at 3.0...
            10  [{'class': 'DATE', 'end': 30, 'start': 16, 'va...  On the night of 28 March, 1959, Krishnamurthi ...
            11  [{'class': 'OTHER_PERSON', 'end': 97, 'start':...  The deceased Collector also initiated a procee...
            12  [{'class': 'PROVISION', 'end': 38, 'start': 24...  In this reference under Section 66 (1) of the ...
            13  [{'class': 'DATE', 'end': 139, 'start': 130, '...  In view of these fact, it can he safely held t...
            14  [{'class': 'OTHER_PERSON', 'end': 16, 'start':...  Shri Vinay Saraf, learned counsel for the appe...
            15  [{'class': 'PROVISION', 'end': 57, 'start': 47...  The other section involved in these appeals is...
            16                                                 []  It was observed that:\n "Of late, crime agains...
            Using default nertag list inside NERdata. ['location', 'city', 'country', 'location_type', 'location_type_exclude']
            {0: 'B-location', 5: 'I-location', 1: 'B-city', 6: 'I-city', 2: 'B-country', 7: 'I-country', 3: 'B-location_type', 8: 'I-location_type', 4: 'B-location_type_exclude', 9: 'I-location_type_exclude', 10: 'Other', -100: 'Special'}

            ###### Dataloader setup  ############################################
            {
            "cfg": "config/train.yml",
            "cfg_name": "model_deverta_legal_doc",
            "data": {
                "I2L": {
                    "-100": "Special",
                    "0": "B-COURT",
                    "1": "B-PETITIONER",
                    "10": "B-PRECEDENT",
                    "11": "B-CASE_NUMBER",
                    "12": "B-WITNESS",
                    "13": "B-OTHER_PERSON",
                    "14": "I-COURT",
                    "15": "I-PETITIONER",
                    "16": "I-RESPONDENT",
                    "17": "I-JUDGE",
                    "18": "I-LAWYER",
                    "19": "I-DATE",
                    "2": "B-RESPONDENT",
                    "20": "I-ORG",
                    "21": "I-GPE",
                    "22": "I-STATUTE",
                    "23": "I-PROVISION",
                    "24": "I-PRECEDENT",
                    "25": "I-CASE_NUMBER",
                    "26": "I-WITNESS",
                    "27": "I-OTHER_PERSON",
                    "28": "Other",
                    "3": "B-JUDGE",
                    "4": "B-LAWYER",
                    "5": "B-DATE",
                    "6": "B-ORG",
                    "7": "B-GPE",
                    "8": "B-STATUTE",
                    "9": "B-PROVISION"
                },
                "L2I": {
                    "B-CASE_NUMBER": 11,
                    "B-COURT": 0,
                    "B-DATE": 5,
                    "B-GPE": 7,
                    "B-JUDGE": 3,
                    "B-LAWYER": 4,
                    "B-ORG": 6,
                    "B-OTHER_PERSON": 13,
                    "B-PETITIONER": 1,
                    "B-PRECEDENT": 10,
                    "B-PROVISION": 9,
                    "B-RESPONDENT": 2,
                    "B-STATUTE": 8,
                    "B-WITNESS": 12,
                    "I-CASE_NUMBER": 25,
                    "I-COURT": 14,
                    "I-DATE": 19,
                    "I-GPE": 21,
                    "I-JUDGE": 17,
                    "I-LAWYER": 18,
                    "I-ORG": 20,
                    "I-OTHER_PERSON": 27,
                    "I-PETITIONER": 15,
                    "I-PRECEDENT": 24,
                    "I-PROVISION": 23,
                    "I-RESPONDENT": 16,
                    "I-STATUTE": 22,
                    "I-WITNESS": 26,
                    "Other": 28,
                    "Special": -100
                },
                "cols": [
                    "ner_list",
                    "text"
                ],
                "cols_remove": [
                    "overflow_to_sample_mapping",
                    "offset_mapping",
                    "ner_list",
                    "text"
                ],
                "cols_required": [
                    "text",
                    "ner_list"
                ],
                "meta_dict": {
                    "I2L": {
                        "-100": "Special",
                        "0": "B-COURT",
                        "1": "B-PETITIONER",
                        "10": "B-PRECEDENT",
                        "11": "B-CASE_NUMBER",
                        "12": "B-WITNESS",
                        "13": "B-OTHER_PERSON",
                        "14": "I-COURT",
                        "15": "I-PETITIONER",
                        "16": "I-RESPONDENT",
                        "17": "I-JUDGE",
                        "18": "I-LAWYER",
                        "19": "I-DATE",
                        "2": "B-RESPONDENT",
                        "20": "I-ORG",
                        "21": "I-GPE",
                        "22": "I-STATUTE",
                        "23": "I-PROVISION",
                        "24": "I-PRECEDENT",
                        "25": "I-CASE_NUMBER",
                        "26": "I-WITNESS",
                        "27": "I-OTHER_PERSON",
                        "28": "Other",
                        "3": "B-JUDGE",
                        "4": "B-LAWYER",
                        "5": "B-DATE",
                        "6": "B-ORG",
                        "7": "B-GPE",
                        "8": "B-STATUTE",
                        "9": "B-PROVISION"
                    },
                    "L2I": {
                        "B-CASE_NUMBER": 11,
                        "B-COURT": 0,
                        "B-DATE": 5,
                        "B-GPE": 7,
                        "B-JUDGE": 3,
                        "B-LAWYER": 4,
                        "B-ORG": 6,
                        "B-OTHER_PERSON": 13,
                        "B-PETITIONER": 1,
                        "B-PRECEDENT": 10,
                        "B-PROVISION": 9,
                        "B-RESPONDENT": 2,
                        "B-STATUTE": 8,
                        "B-WITNESS": 12,
                        "I-CASE_NUMBER": 25,
                        "I-COURT": 14,
                        "I-DATE": 19,
                        "I-GPE": 21,
                        "I-JUDGE": 17,
                        "I-LAWYER": 18,
                        "I-ORG": 20,
                        "I-OTHER_PERSON": 27,
                        "I-PETITIONER": 15,
                        "I-PRECEDENT": 24,
                        "I-PROVISION": 23,
                        "I-RESPONDENT": 16,
                        "I-STATUTE": 22,
                        "I-WITNESS": 26,
                        "Other": 28,
                        "Special": -100
                    },
                    "NCLASS": 14,
                    "NCLASS_BOI": 29,
                    "NLABEL_TOTAL": 29,
                    "ner_dataframe_cols": [
                        "text",
                        "ner_list"
                    ],
                    "ner_fields": [
                        "start",
                        "end",
                        "class",
                        "value"
                    ],
                    "nertag_list": [
                        "COURT",
                        "PETITIONER",
                        "RESPONDENT",
                        "JUDGE",
                        "LAWYER",
                        "DATE",
                        "ORG",
                        "GPE",
                        "STATUTE",
                        "PROVISION",
                        "PRECEDENT",
                        "CASE_NUMBER",
                        "WITNESS",
                        "OTHER_PERSON"
                    ],
                    "token_BOI": [
                        "B",
                        "I",
                        "Other"
                    ]
                },
                "nclass": 14,
                "ner_format": [
                    "start",
                    "end",
                    "class",
                    "value"
                ]
            },
            "dataloader_name": "data_legalDoc_load_datasplit",
            "datamapper_name": "data_legalDoc_load_metadict",
            "dirin": "ztmp/data/ner/legaldoc/",
            "dirout": "ztmp/exp_deberta_legal_doc/20240602/110950-ner_deberta-5",
            "hf_args_model": {
                "model_name": "microsoft/deberta-v3-base",
                "num_labels": 29
            },
            "hf_args_train": {
                "evaluation_strategy": "epoch",
                "gradient_accumulation_steps": 1,
                "learning_rate": 1e-05,
                "logging_steps": 4,
                "logging_strategy": "epoch",
                "max_grad_norm": 2,
                "max_steps": -1,
                "num_train_epochs": 1,
                "optim": "adamw_hf",
                "output_dir": "ztmp/exp_deberta_legal_doc/log_train",
                "per_device_train_batch_size": 64,
                "save_steps": 4,
                "save_strategy": "epoch",
                "warmup_ratio": 0.2
            },
            "model_name": "microsoft/deberta-v3-base",
            "model_path": "model_deberta",
            "model_type": "deberta",
            "n_train": 5,
            "n_val": 2
            }
            Map: 100%|█████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 405.09 examples/s]
            Dataset({
                features: ['input_ids', 'token_type_ids', 'attention_mask', 'labels'],
                num_rows: 5
            })
            {
            "cfg": "config/train.yml",
            "cfg_name": "model_deverta_legal_doc",
            "data": {
                "I2L": {
                    "-100": "Special",
                    "0": "B-COURT",
                    "1": "B-PETITIONER",
                    "10": "B-PRECEDENT",
                    "11": "B-CASE_NUMBER",
                    "12": "B-WITNESS",
                    "13": "B-OTHER_PERSON",
                    "14": "I-COURT",
                    "15": "I-PETITIONER",
                    "16": "I-RESPONDENT",
                    "17": "I-JUDGE",
                    "18": "I-LAWYER",
                    "19": "I-DATE",
                    "2": "B-RESPONDENT",
                    "20": "I-ORG",
                    "21": "I-GPE",
                    "22": "I-STATUTE",
                    "23": "I-PROVISION",
                    "24": "I-PRECEDENT",
                    "25": "I-CASE_NUMBER",
                    "26": "I-WITNESS",
                    "27": "I-OTHER_PERSON",
                    "28": "Other",
                    "3": "B-JUDGE",
                    "4": "B-LAWYER",
                    "5": "B-DATE",
                    "6": "B-ORG",
                    "7": "B-GPE",
                    "8": "B-STATUTE",
                    "9": "B-PROVISION"
                },
                "L2I": {
                    "B-CASE_NUMBER": 11,
                    "B-COURT": 0,
                    "B-DATE": 5,
                    "B-GPE": 7,
                    "B-JUDGE": 3,
                    "B-LAWYER": 4,
                    "B-ORG": 6,
                    "B-OTHER_PERSON": 13,
                    "B-PETITIONER": 1,
                    "B-PRECEDENT": 10,
                    "B-PROVISION": 9,
                    "B-RESPONDENT": 2,
                    "B-STATUTE": 8,
                    "B-WITNESS": 12,
                    "I-CASE_NUMBER": 25,
                    "I-COURT": 14,
                    "I-DATE": 19,
                    "I-GPE": 21,
                    "I-JUDGE": 17,
                    "I-LAWYER": 18,
                    "I-ORG": 20,
                    "I-OTHER_PERSON": 27,
                    "I-PETITIONER": 15,
                    "I-PRECEDENT": 24,
                    "I-PROVISION": 23,
                    "I-RESPONDENT": 16,
                    "I-STATUTE": 22,
                    "I-WITNESS": 26,
                    "Other": 28,
                    "Special": -100
                },
                "cols": [
                    "ner_list",
                    "text"
                ],
                "cols_remove": [
                    "overflow_to_sample_mapping",
                    "offset_mapping",
                    "ner_list",
                    "text"
                ],
                "cols_required": [
                    "text",
                    "ner_list"
                ],
                "meta_dict": {
                    "I2L": {
                        "-100": "Special",
                        "0": "B-COURT",
                        "1": "B-PETITIONER",
                        "10": "B-PRECEDENT",
                        "11": "B-CASE_NUMBER",
                        "12": "B-WITNESS",
                        "13": "B-OTHER_PERSON",
                        "14": "I-COURT",
                        "15": "I-PETITIONER",
                        "16": "I-RESPONDENT",
                        "17": "I-JUDGE",
                        "18": "I-LAWYER",
                        "19": "I-DATE",
                        "2": "B-RESPONDENT",
                        "20": "I-ORG",
                        "21": "I-GPE",
                        "22": "I-STATUTE",
                        "23": "I-PROVISION",
                        "24": "I-PRECEDENT",
                        "25": "I-CASE_NUMBER",
                        "26": "I-WITNESS",
                        "27": "I-OTHER_PERSON",
                        "28": "Other",
                        "3": "B-JUDGE",
                        "4": "B-LAWYER",
                        "5": "B-DATE",
                        "6": "B-ORG",
                        "7": "B-GPE",
                        "8": "B-STATUTE",
                        "9": "B-PROVISION"
                    },
                    "L2I": {
                        "B-CASE_NUMBER": 11,
                        "B-COURT": 0,
                        "B-DATE": 5,
                        "B-GPE": 7,
                        "B-JUDGE": 3,
                        "B-LAWYER": 4,
                        "B-ORG": 6,
                        "B-OTHER_PERSON": 13,
                        "B-PETITIONER": 1,
                        "B-PRECEDENT": 10,
                        "B-PROVISION": 9,
                        "B-RESPONDENT": 2,
                        "B-STATUTE": 8,
                        "B-WITNESS": 12,
                        "I-CASE_NUMBER": 25,
                        "I-COURT": 14,
                        "I-DATE": 19,
                        "I-GPE": 21,
                        "I-JUDGE": 17,
                        "I-LAWYER": 18,
                        "I-ORG": 20,
                        "I-OTHER_PERSON": 27,
                        "I-PETITIONER": 15,
                        "I-PRECEDENT": 24,
                        "I-PROVISION": 23,
                        "I-RESPONDENT": 16,
                        "I-STATUTE": 22,
                        "I-WITNESS": 26,
                        "Other": 28,
                        "Special": -100
                    },
                    "NCLASS": 14,
                    "NCLASS_BOI": 29,
                    "NLABEL_TOTAL": 29,
                    "ner_dataframe_cols": [
                        "text",
                        "ner_list"
                    ],
                    "ner_fields": [
                        "start",
                        "end",
                        "class",
                        "value"
                    ],
                    "nertag_list": [
                        "COURT",
                        "PETITIONER",
                        "RESPONDENT",
                        "JUDGE",
                        "LAWYER",
                        "DATE",
                        "ORG",
                        "GPE",
                        "STATUTE",
                        "PROVISION",
                        "PRECEDENT",
                        "CASE_NUMBER",
                        "WITNESS",
                        "OTHER_PERSON"
                    ],
                    "token_BOI": [
                        "B",
                        "I",
                        "Other"
                    ]
                },
                "nclass": 14,
                "ner_format": [
                    "start",
                    "end",
                    "class",
                    "value"
                ]
            },
            "dataloader_name": "data_legalDoc_load_datasplit",
            "datamapper_name": "data_legalDoc_load_metadict",
            "dirin": "ztmp/data/ner/legaldoc/",
            "dirout": "ztmp/exp_deberta_legal_doc/20240602/110950-ner_deberta-5",
            "hf_args_model": {
                "model_name": "microsoft/deberta-v3-base",
                "num_labels": 29
            },
            "hf_args_train": {
                "evaluation_strategy": "epoch",
                "gradient_accumulation_steps": 1,
                "learning_rate": 1e-05,
                "logging_steps": 4,
                "logging_strategy": "epoch",
                "max_grad_norm": 2,
                "max_steps": -1,
                "num_train_epochs": 1,
                "optim": "adamw_hf",
                "output_dir": "ztmp/exp_deberta_legal_doc/log_train",
                "per_device_train_batch_size": 64,
                "save_steps": 4,
                "save_strategy": "epoch",
                "warmup_ratio": 0.2
            },
            "model_name": "microsoft/deberta-v3-base",
            "model_path": "model_deberta",
            "model_type": "deberta",
            "n_train": 5,
            "n_val": 2
            }
            Map: 100%|█████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 218.12 examples/s]
            Dataset({
                features: ['input_ids', 'token_type_ids', 'attention_mask', 'labels'],
                num_rows: 2
            })

            ######### DataCollator #########################################
            You're using a DebertaV2TokenizerFast tokenizer. Please note that with a fast tokenizer, using the `__call__` method is faster than using a method to encode the text followed by a call to the `pad` method to get a padded encoding.
            {'input_ids': tensor([[     1,    287,    819,    285,    589,    996,   7236,    293,    262,
                    18393,    314,    299,   1649,    265,   4814,    260,    376,    261,
                    4230,    261,   5422,    261,   2429,    277,   4353,    626,    265,
                    102414,   2122,    914,    265,    319,    266,   1456,   2104,    269,
                    7809,    288,    845,    260,   1297,    265,  89941,    280,    268,
                    1089,    550,    261,   1859,  19843,   4290,   3761,    272,    278,
                        284,   1144,    264,   2183,    292,   7347,    261,  27353,    429,
                    1422,    260,    277,    262,   1599,    265,    315,   6898,    266,
                    1241,   2780,    269,    552,    293,    381,    277,    272,   1456,
                    2104,    260,      2],
                    [     1,    383,    284,    327,    921,    786,    336,  78624,   2569,
                    22800,    938,   1510,    309,  37251,    616,  12948,    309,   9764,
                    1510,    309,  22800,    616,    524,    309,   1504,  34916,    585,
                        260,  40511,    271,  13010,    265,   4286,    525,   4052,    320,
                    22800,   1504,  46820,    261,   1346,    271,    547,    271,   5697,
                        265,    262,  11740,   2464,   7113,    292,  11428,  49015,   1398,
                    7552,    260,      2,      2,      2,      2,      2,      2,      2,
                        2,      2,      2,      2,      2,      2,      2,      2,      2,
                        2,      2,      2,      2,      2,      2,      2,      2,      2,
                        2,      2,      2]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'labels': tensor([[-100,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,   28,   28,    6,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,    6,   20,   20,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28, -100],
                    [-100,   28,   28,   28,   28,   28,   28,   13,   28,   28,   28,   28,
                    28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,   28,
                    28,   28,   28,   28,   13,   27,   27,   28, -100, -100, -100, -100,
                    -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100,
                    -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100]])}

            ######### Model : Init #########################################
            Some weights of DebertaV2ForTokenClassification were not initialized from the model checkpoint at microsoft/deberta-v3-base and are newly initialized: ['classifier.bias', 'classifier.weight']
            You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.

            ######### Model : Training start ##############################
            {'loss': 3.6424, 'grad_norm': 27.369539260864258, 'learning_rate': 0.0, 'epoch': 1.0}                        
            {'eval_loss': 3.6029818058013916, 'eval_precision': 0.0, 'eval_recall': 0.0, 'eval_f1': 0.0, 'eval_accuracy': 0.0072992700729927005, 'eval_runtime': 1.9394, 'eval_samples_per_second': 1.031, 'eval_steps_per_second': 0.516, 'epoch': 1.0}
            {'train_runtime': 13.7533, 'train_samples_per_second': 0.364, 'train_steps_per_second': 0.073, 'train_loss': 3.6424152851104736, 'epoch': 1.0}                                                                            
            100%|██████████████████████████████████████████████████████████████████████████| 1/1 [00:13<00:00, 13.76s/it]
            {'model_name': 'microsoft/deberta-v3-base', 'dataloader_name': 'data_legalDoc_load_datasplit', 'datamapper_name': 'data_legalDoc_load_metadict', 'n_train': 5, 'n_val': 2, 'hf_args_train': {'output_dir': 'ztmp/exp_deberta_legal_doc/log_train', 'per_device_train_batch_size': 64, 'gradient_accumulation_steps': 1, 'optim': 'adamw_hf', 'save_steps': 4, 'logging_steps': 4, 'learning_rate': 1e-05, 'max_grad_norm': 2, 'max_steps': -1, 'num_train_epochs': 1, 'warmup_ratio': 0.2, 'evaluation_strategy': 'epoch', 'logging_strategy': 'epoch', 'save_strategy': 'epoch'}, 'hf_args_model': {'model_name': 'microsoft/deberta-v3-base', 'num_labels': 29}, 'cfg': 'config/train.yml', 'cfg_name': 'model_deverta_legal_doc', 'model_path': 'model_deberta', 'model_type': 'deberta', 'dirin': 'ztmp/data/ner/legaldoc/', 'dirout': 'ztmp/exp_deberta_legal_doc/20240602/110950-ner_deberta-5', 'data': {'cols': ['ner_list', 'text'], 'cols_required': ['text', 'ner_list'], 'ner_format': ['start', 'end', 'class', 'value'], 'cols_remove': ['overflow_to_sample_mapping', 'offset_mapping', 'ner_list', 'text'], 'meta_dict': {'nertag_list': ['COURT', 'PETITIONER', 'RESPONDENT', 'JUDGE', 'LAWYER', 'DATE', 'ORG', 'GPE', 'STATUTE', 'PROVISION', 'PRECEDENT', 'CASE_NUMBER', 'WITNESS', 'OTHER_PERSON'], 'NCLASS': 14, 'NCLASS_BOI': 29, 'NLABEL_TOTAL': 29, 'token_BOI': ['B', 'I', 'Other'], 'L2I': {'B-COURT': 0, 'I-COURT': 14, 'B-PETITIONER': 1, 'I-PETITIONER': 15, 'B-RESPONDENT': 2, 'I-RESPONDENT': 16, 'B-JUDGE': 3, 'I-JUDGE': 17, 'B-LAWYER': 4, 'I-LAWYER': 18, 'B-DATE': 5, 'I-DATE': 19, 'B-ORG': 6, 'I-ORG': 20, 'B-GPE': 7, 'I-GPE': 21, 'B-STATUTE': 8, 'I-STATUTE': 22, 'B-PROVISION': 9, 'I-PROVISION': 23, 'B-PRECEDENT': 10, 'I-PRECEDENT': 24, 'B-CASE_NUMBER': 11, 'I-CASE_NUMBER': 25, 'B-WITNESS': 12, 'I-WITNESS': 26, 'B-OTHER_PERSON': 13, 'I-OTHER_PERSON': 27, 'Other': 28, 'Special': -100}, 'I2L': {'0': 'B-COURT', '14': 'I-COURT', '1': 'B-PETITIONER', '15': 'I-PETITIONER', '2': 'B-RESPONDENT', '16': 'I-RESPONDENT', '3': 'B-JUDGE', '17': 'I-JUDGE', '4': 'B-LAWYER', '18': 'I-LAWYER', '5': 'B-DATE', '19': 'I-DATE', '6': 'B-ORG', '20': 'I-ORG', '7': 'B-GPE', '21': 'I-GPE', '8': 'B-STATUTE', '22': 'I-STATUTE', '9': 'B-PROVISION', '23': 'I-PROVISION', '10': 'B-PRECEDENT', '24': 'I-PRECEDENT', '11': 'B-CASE_NUMBER', '25': 'I-CASE_NUMBER', '12': 'B-WITNESS', '26': 'I-WITNESS', '13': 'B-OTHER_PERSON', '27': 'I-OTHER_PERSON', '28': 'Other', '-100': 'Special'}, 'ner_fields': ['start', 'end', 'class', 'value'], 'ner_dataframe_cols': ['text', 'ner_list']}, 'L2I': {'B-COURT': 0, 'I-COURT': 14, 'B-PETITIONER': 1, 'I-PETITIONER': 15, 'B-RESPONDENT': 2, 'I-RESPONDENT': 16, 'B-JUDGE': 3, 'I-JUDGE': 17, 'B-LAWYER': 4, 'I-LAWYER': 18, 'B-DATE': 5, 'I-DATE': 19, 'B-ORG': 6, 'I-ORG': 20, 'B-GPE': 7, 'I-GPE': 21, 'B-STATUTE': 8, 'I-STATUTE': 22, 'B-PROVISION': 9, 'I-PROVISION': 23, 'B-PRECEDENT': 10, 'I-PRECEDENT': 24, 'B-CASE_NUMBER': 11, 'I-CASE_NUMBER': 25, 'B-WITNESS': 12, 'I-WITNESS': 26, 'B-OTHER_PERSON': 13, 'I-OTHER_PERSON': 27, 'Other': 28, 'Special': -100}, 'I2L': {'0': 'B-COURT', '14': 'I-COURT', '1': 'B-PETITIONER', '15': 'I-PETITIONER', '2': 'B-RESPONDENT', '16': 'I-RESPONDENT', '3': 'B-JUDGE', '17': 'I-JUDGE', '4': 'B-LAWYER', '18': 'I-LAWYER', '5': 'B-DATE', '19': 'I-DATE', '6': 'B-ORG', '20': 'I-ORG', '7': 'B-GPE', '21': 'I-GPE', '8': 'B-STATUTE', '22': 'I-STATUTE', '9': 'B-PROVISION', '23': 'I-PROVISION', '10': 'B-PRECEDENT', '24': 'I-PRECEDENT', '11': 'B-CASE_NUMBER', '25': 'I-CASE_NUMBER', '12': 'B-WITNESS', '26': 'I-WITNESS', '13': 'B-OTHER_PERSON', '27': 'I-OTHER_PERSON', '28': 'Other', '-100': 'Special'}, 'nclass': 14}, 'metrics_trainer': {'train_runtime': 13.7533, 'train_samples_per_second': 0.364, 'train_steps_per_second': 0.073, 'total_flos': 214401189240.0, 'train_loss': 3.6424152851104736, 'epoch': 1.0}}
            <_io.TextIOWrapper name='ztmp/exp_deberta_legal_doc/20240602/110950-ner_deberta-5/config.json' mode='w' encoding='UTF-8'>

            ######### Model : Eval Predict  ######################################
            100%|██████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.15s/it]
            pred_proba:  [[[ 4.5905128e-02 -3.5802633e-01  4.3503410e-01 ..
            labels:  [[-100   28   28   28   28   28   28   28   28   2
            pred_class:  [[ 4  4  4  5 22 15 22 22  3  4 22  5 22 22  5 22 
            {'text': "\n\n(7) On specific query by the Bench about an entry of Rs. 1,31,37,500 on deposit side of Hongkong Bank account of which a photo copy is appearing at p. 40 of assessee's paper book, learned authorised representative submitted that it was related to loan from broker, Rahul & Co. on the basis of his submission a necessary mark is put by us on that photo copy.", 'offset_mapping': [[[0, 0], [2, 3], [3, 4], [4, 5], [5, 8], [8, 17], [17, 23], [23, 26], [26, 30], [30, 36], [36, 42], [42, 45], [45, 51], [51, 54], [54, 57], [57, 58], [58, 60], [60, 61], [61, 63], [63, 64], [64, 66], [66, 67], [67, 70], [70, 73], [73, 81], [81, 86], [86, 89], [89, 98], [98, 103], [103, 111], [111, 114], [114, 120], [120, 122], [122, 128], [128, 133], [133, 136], [136, 146], [146, 149], [149, 151], [151, 152], [152, 155], [155, 158], [158, 167], [167, 168], [168, 169], [169, 175], [175, 180], [180, 181], [181, 189], [189, 200], [200, 215], [215, 225], [225, 230], [230, 233], [233, 237], [237, 245], [245, 248], [248, 253], [253, 258], [258, 265], [265, 266], [266, 272], [272, 274], [274, 277], [277, 278], [278, 281], [281, 285], [285, 291], [291, 294], [294, 298], [298, 309], [309, 311], [311, 321], [321, 326], [326, 329], [329, 333], [333, 336], [336, 339], [339, 342], [342, 347], [347, 353], [353, 358], [358, 359], [0, 0]]]} [ 4  4  4  5 22 15 22 22  3  4 22  5 22 22  5 22  4 22  4 22  4  0  4 22
            22 22 22  4 22 22 22  8  5 22 22 22 22 22 22 22  4 22  9  0  5 15 22 22
            1 22 22 22 22 22 22 22 22 22 22  9 22  4 22  4 15  9  5  5  5 15 22 15
            22 15 22 22 22 22 22 22 22 22  7  4] 84 84
            {'text': 'He was also asked whether Agya <span class="hidden_text" id="span_5"> CRA No.326-DB of 1998 6</span> Kaur, mother-in-law of the deceased lived separately from Tarlochan Singh.', 'offset_mapping': [[[0, 0], [0, 2], [2, 6], [6, 11], [11, 17], [17, 25], [25, 27], [27, 30], [30, 32], [32, 36], [36, 42], [42, 43], [43, 44], [44, 50], [50, 51], [51, 55], [55, 56], [56, 59], [59, 60], [60, 61], [61, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 73], [73, 76], [76, 77], [77, 80], [80, 81], [81, 83], [83, 86], [86, 91], [91, 93], [93, 94], [94, 95], [95, 99], [99, 100], [100, 105], [105, 106], [106, 113], [113, 114], [114, 116], [116, 117], [117, 120], [120, 123], [123, 127], [127, 136], [136, 142], [142, 153], [153, 158], [158, 162], [162, 166], [166, 168], [168, 174], [174, 175], [0, 0]]]} [ 4  4 22 22 22 22 22  4 10 22  4  5  5  4 15 22 15  4  5 28 15 15  4  5
            15 15  5 22  4  4 15 15  5  9 10 22 15 22 22 22  4 22  5 15 22 22 22  4
            22 15  5  4 22 22 22 15  4 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14
            14 14 14 14 14 14 14 14 14 14 14 14] 84 57

            ######### Model : Eval Metrics #######################################
            {'accuracy': {'ORG': 0.0}, 'accuracy_total': 0.0}
            ztmp/exp_deberta_legal_doc/20240602/110950-ner_deberta-5/dfval_pred_ner.parquet
                                                        ner_list  ...                                           accuracy
            0  [{'class': 'ORG', 'end': 103, 'start': 90, 'va...  ...  {'accuracy': {'ORG': 0.0}, 'accuracy_total': 0.0}
            1  [{'class': 'OTHER_PERSON', 'end': 30, 'start':...  ...  {'accuracy': {'OTHER_PERSON': 0.0}, 'accuracy_...

            [2 rows x 7 columns]




##### Copy paste the sddout of alll you runs.
== easy to check/ to remember...



"""