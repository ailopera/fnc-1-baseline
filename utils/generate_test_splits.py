import random
import os
from collections import defaultdict
import csv

def generate_hold_out_split (dataset, training = 0.8, base_dir="splits"):
    r = random.Random()
    r.seed(1489215)

    article_ids = list(dataset.articles.keys())  # get a list of article ids
    r.shuffle(article_ids)  # and shuffle that list


    training_ids = article_ids[:int(training * len(article_ids))]
    hold_out_ids = article_ids[int(training * len(article_ids)):]
    
    print("Noticias utilizadas para el train: ", len(training_ids))
    print("Noticias utilizadas para el test: ", len(hold_out_ids))
    
    dataset_path = "/home/Operador/tensor_project/data/fnc-1-original/finalDatasets/total_data_aggregated.csv"
    outputTrainPath = "train_partition.csv"
    outputTestPath = "test_partition.csv"

    with open(dataset_path, 'r') as data, open(outputTrainPath, 'w') as trainFile, open(outputTestPath, 'w') as testFile:
        print(">> Fichero de train generado:", outputTrainPath)
        print(">> Fichero de test generado:", outputTestPath)
        
        fieldnames = ["Headline","ArticleBody","Stance","BodyIDS"]
        trainWriter = csv.DictWriter(trainFile, fieldnames=fieldnames)
        testWriter = csv.DictWriter(testFile, fieldnames=fieldnames)
        
        # Escribimos los headers de los dos datasets
        testWriter.writeheader()
        trainWriter.writeheader()
        validationWriter.writeheader()
        
        # Vamos recorriendo el fichero de datos agregados y encaminamos las muestras al dataset correspondiente
        for line in csv.reader(data, delimiter=','):
            
            row = { "Headline": line[0],
            "ArticleBody": line[1],
            "Stance": line[2],
            "BodyIDS": line[3]}
            
            bodyIds = int(line[3]) if not line[3] == "BodyIDS" else -1
            if bodyIds in training_ids:
                trainWriter.writerow(row)
            elif bodyIds in hold_out_ids:
                validationWriter.writerow(row)
            else: 
                testWriter.writerow(row)
                print(">> Se ha encontrado un id fuera de la lista")
                print(">>> line[3] ", line[3] )
    
    # write the split body ids out to files for future use
    # with open(base_dir+ "/"+ "training_ids.txt", "w+") as f:
    #     f.write("\n".join([str(id) for id in training_ids]))

    # with open(base_dir+ "/"+ "hold_out_ids.txt", "w+") as f:
    #     f.write("\n".join([str(id) for id in hold_out_ids]))



def read_ids(file,base):
    ids = []
    with open(base+"/"+file,"r") as f:
        for line in f:
           ids.append(int(line))
        return ids


def kfold_split(dataset, training = 0.8, n_folds = 10, base_dir="splits"):
    if not (os.path.exists(base_dir+ "/"+ "training_ids.txt")
            and os.path.exists(base_dir+ "/"+ "hold_out_ids.txt")):
        generate_hold_out_split(dataset,training,base_dir)

    training_ids = read_ids("training_ids.txt", base_dir)
    hold_out_ids = read_ids("hold_out_ids.txt", base_dir)

    folds = []
    for k in range(n_folds):
        folds.append(training_ids[int(k*len(training_ids)/n_folds):int((k+1)*len(training_ids)/n_folds)])

    return folds,hold_out_ids


def get_stances_for_folds(dataset,folds,hold_out):
    stances_folds = defaultdict(list)
    stances_hold_out = []
    for stance in dataset.stances:
        if stance['Body ID'] in hold_out:
            stances_hold_out.append(stance)
        else:
            fold_id = 0
            for fold in folds:
                if stance['Body ID'] in fold:
                    stances_folds[fold_id].append(stance)
                fold_id += 1

    return stances_folds,stances_hold_out
