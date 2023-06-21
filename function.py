import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.utils import resample
from sklearn import preprocessing
# Import required libraries
from keras.models import Sequential
from keras.layers import Dense,Embedding,Dropout,Flatten,MaxPooling1D,LSTM

def load_model(name):
    from keras.models import model_from_json
    
    arq_json = 'Models/' + name + '.json'
    json_file = open(arq_json,'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    
    arq_h5 = 'Models/' + name + '.h5'
    loaded_model.load_weights(arq_h5)
    
    print('Model loaded')
    
    return loaded_model

def detect_anomaly(csv_path, model):
    # read data
    # cols = list(pd.read_csv(csv_path, nrows=1))

    data = pd.read_csv(csv_path)
            #    usecols =[i for i in cols if i != 'dst_ip' and i != 'FID' 
            #              and i != 'SimillarHTTP' and i != 'Unnamed: 0' and i != ' Inbound'])
    drop_columns = [ # this list includes all spellings across CIC NIDS datasets
        "dst_ip",
        "FID",
        # "Unnamed: 0", "Inbound", "SimillarHTTP" # CIC-DDoS other undocumented columns
    ]
    data.drop(columns=drop_columns, inplace=True, errors='ignore')    
    source_ip = data['src_ip']
    data = data.drop("src_ip", axis=1)
    
    # only for data from dataset
    # data = data.drop(' Label', axis=1)
    
    # preprocess
    def string2numeric_hash(text):
        import hashlib
        return int(hashlib.md5(text).hexdigest()[:8], 16)

    # Flows Packet/s e Bytes/s - Replace infinity by 0
    data = data.replace('Infinity','0')
    data = data.replace(np.inf,0)
    #data = data.replace('nan','0')
    data['flow_pkts_s'] = pd.to_numeric(data['flow_pkts_s'])

    data['flow_byts_s'] = data['flow_byts_s'].fillna(0)
    data['flow_byts_s'] = pd.to_numeric(data['flow_byts_s'])

    #Timestamp - Drop day, then convert hour, minute and seconds to hashing 
    colunaTime = pd.DataFrame(data['timestamp'].str.split(' ',1).tolist(), columns = ['dia','horas'])
    # colunaTime = pd.DataFrame(colunaTime['horas'].str.split('.',1).tolist(),columns = ['horas','milisec'])
    stringHoras = pd.DataFrame(colunaTime['horas'].str.encode('utf-8'))
    data['timestamp'] = pd.DataFrame(stringHoras['horas'].apply(string2numeric_hash))#colunaTime['horas']
    del colunaTime,stringHoras


    predictions = model.predict(data)
    predictions = np.argmax(predictions, axis=1)

    predictions = pd.DataFrame({'label': predictions})
    result = pd.concat([source_ip, predictions], axis=1)

    result = result[result['label'] != 0]


    # Create a DataFrame of anomalies
#     anomaly_df = pd.DataFrame()
#     for i in range(len(predictions)):
#         if predictions[i] != "0":
#             anomaly_df = anomaly_df.append({' Source IP': source_ip[i], "Label": predictions[i]}, ignore_index=True)

    # anomaly_df = np.array([])
    # for i in range(len(predictions)):
    #     if predictions[i] != 0:
    #         anomaly_df = np.append(anomaly_df, [source_ip[i], predictions[i]])
    
    # Print the IP address of the unique anomalies
#     print(anomaly_df["IP"].unique())
    # anomaly_df = anomaly_df.reshape(-1, 2)
    label_map = {
        0: "BENIGN",
        1: "DrDoS_DNS",
        2: "DrDoS_LDAP",
        3: "DrDoS_MSSQL",
        4: "DrDoS_NTP",
        5: "DrDoS_NetBIOS",
        6: "DrDoS_SNMP",
        7: "DrDoS_UDP",
        8: "LDAP",
        9: "MSSQL",
        10: "NetBIOS",
        11: "Portmap",
        12: "Syn",
        13: "TFTP",
        14: "UDP",
        15: "UDP-lag",
        16: "UDPLag",
        17: "WebDDoS",
    }

    # result = result.rename(columns={"label": label_map})
    result["label"] = result["label"].map(label_map)

    import json
    return json.dumps(result.to_dict('records'))
    # return result.to_json()
    # unique_values = np.unique(anomaly_df, axis=0)

    # # Print the results in a fancy format.
    # print('Source IP | anomaly')
    # print('===================')
    # for row in unique_values:
    #     print(f"{row[0]} | {label_map[row[1]]}")

