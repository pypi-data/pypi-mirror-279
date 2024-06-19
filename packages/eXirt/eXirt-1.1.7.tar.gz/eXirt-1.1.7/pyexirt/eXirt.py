#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 10:40:10 2023

@author: josedesousa
"""

import math
import pandas as pd
import matplotlib.pyplot as plt
from numpy import linspace

from pickle import FALSE
import time
import os
import importlib.util

import warnings
warnings.filterwarnings("ignore")

package_name = 'wget'
spec = importlib.util.find_spec(package_name)
if spec is None:
    os.system("pip install wget")

package_name = 'openml'
spec = importlib.util.find_spec(package_name)
if spec is None:
    os.system("pip install openml")
    
package_name = 'rpy2'
spec = importlib.util.find_spec(package_name)
if spec is None:
    os.system("pip install rpy2")

package_name = 'catsim'
spec = importlib.util.find_spec(package_name)
if spec is None:
    os.system("pip install catsim")

import platform
import wget

import openml
import pandas as pd
import statistics
import numpy as np
import random
import copy



from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics



#if os.path.isfile(os.path.join(os.getcwd(),'decodIRT_MLtIRT.py')) == False:
#                  wget.download('https://raw.githubusercontent.com/josesousaribeiro/eXirt/main/eXirt/decodIRT_MLtIRT.py')

#if os.path.isfile(os.path.join(os.getcwd(),'decodIRT_analysis.py')) == False:
#                  wget.download('https://raw.githubusercontent.com/josesousaribeiro/eXirt/main/eXirt/decodIRT_analysis.py')


def normalize(df): #min_max
    # copy the dataframe
    df_norm = df.copy()
    # apply min-max scaling
    for column in df_norm.columns:
        if(len(df_norm[column].unique()) > 1): #fix NaN generation
          df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())
        else:
          df_norm[column] = 0
    return df_norm

#trata outliers dificudade
def trataOutliersDif(listDif):
  limMin = -3
  limMax =  3
  #limMin = -10
  #limMax =  10
  for i, val in enumerate(listDif):
    if val > limMax:
      listDif[i] = limMax
    else:
      if val < limMin:
        listDif[i] = limMin
  return listDif

def trataOutliersDis(listDis):
  limMin = -3
  limMax = 3
  #limMin = -2.5
  #limMax =  2.5
  #limMin = -10
  #limMax =  10
  for i, val in enumerate(listDis):
    if val > limMax:
      listDis[i] = limMax
    else:
      if val < limMin:
        listDis[i] = limMin
  return listDis

def trataOutliersGues(listGues):
  limMin = 0
  limMax =  1
  #limMin = -10
  #limMax =  10
  for i, val in enumerate(listGues):
    if val > limMax:
      listGues[i] = limMax
    else:
      if val < limMin:
        listGues[i] = limMin
  return listGues

def calcICC(a, b, c,theta):
  #return c + (1 - c) * (1/(1+math.e**(-a*(x_axis - b))))
  return c + ((1 - c) / (1 + math.e ** (-a * (theta - b))))

def plotICC(path_of_irt_item_param, path_out_plot, title):
  line = 0.3
  name_file = path_of_irt_item_param
  print('reading: '+name_file)
  dataset = pd.read_csv(name_file)
  dataset = dataset.drop('Unnamed: 0',axis=1)

  dataset['Dificuldade'] = trataOutliersDif(dataset['Dificuldade'])
  dataset['Discriminacao'] = trataOutliersDis(dataset['Discriminacao'])
  dataset['Adivinhacao'] = trataOutliersGues(dataset['Adivinhacao'])

  plt.figure(figsize=(6,5))
  for i in dataset.index:
    a = dataset['Discriminacao'][i]
    b = dataset['Dificuldade'][i]
    c = dataset['Adivinhacao'][i]
    x_axis = linspace(-6, 6, 100)
    y_axis = calcICC(a,b,c,x_axis)

    if a >= 0:
      plt.plot(x_axis, y_axis,color='SeaGreen',linewidth=line)
    else:
      plt.plot(x_axis, y_axis,color='LightCoral',linewidth=line)
  a = dataset['Discriminacao'].mean()
  b = dataset['Dificuldade'].mean()
  c = dataset['Adivinhacao'].mean()
  k = 0
  if a < 0:
    k = 0.5
  x_axis = linspace(-6,6, 100)
  y_axis = calcICC(a,b,c,x_axis)

  if a >= 0:
    plt.text(-0,0.1+k,'Guessing: '+str(round(c,2)),fontsize=14)
  plt.text(0,0.2+k,'Discrimination: '+str(round(a,2)),fontsize=14)
  plt.text(0,0.3+k,'Difficulty: '+str(round(b,2)),fontsize=14)
  plt.plot(x_axis, y_axis,color='black')
  plt.ylabel('Probability of Correct Response P(Θ)',fontsize=16)
  plt.xlabel('Ability θ',fontsize=16)
  plt.title(title,fontsize=16)

  plt.savefig(path_out_plot)


IN_COLAB = True


class Explainer():
  # -*- coding: utf-8 -*-
  """
  Created on Sat Oct 18 21:21:11 2021
  @author: Jose Ribeiro
  This class performs all ensemble-based black box machine learning model explanation processes using advanced IRT techniques.
  
  Link: https://github.com/josesousaribeiro/eXirt
  
  Requirements: RStudio installed - https://cran.r-project.org/bin/windows/base/
  """
  

  def dirByDataset(self, datasetName):
      if os.path.isdir(self.path_content) == False:
          os.mkdir(self.path_content)
      if os.path.isdir(self.path_content+self.path_fig+datasetName) == False:
          os.mkdir(self.path_content+self.path_fig+datasetName)
      if os.path.isdir(self.path_content+self.path_csv+datasetName) == False:
        os.mkdir(self.path_content+self.path_csv+datasetName)
      if os.path.isdir(self.path_content+self.path_model+datasetName) == False:
          os.mkdir(self.path_content+self.path_model+datasetName)
      if os.path.isdir(self.path_content+self.path_irt+datasetName) == False:
        os.mkdir(self.path_content+self.path_irt+datasetName)

  def __init__(self):
    ############################## PATH FILE ###################################
    
    if platform.system() == 'Windows':
       self.bar = '\\'
    else:
       self.bar =  '/'
    
    self.path_content_simple = self.bar+'content_eXirt'
    self.path_content = os.getcwd()+self.path_content_simple
    self.path_fig = self.bar+'out_fig'
    self.path_csv = self.bar+'out_csv'
    self.path_model = self.bar+'out_model'
    self.path_irt = self.bar+'out_irt' 
    self.path_dataset = self.bar+'*'

    
    self.dirByDataset('')
    
    ############################## GENERAL CONTROL #############################
    self.proposal_1_pool = 1
    self.proposal_2_loop = 2
    self.exec_proposal = self.proposal_2_loop

    # verbose
    self.verbose = False
    self.verbose_graph = False

    self.download_files = True

    # performance
    self.exec_accuracy = 1
    self.exec_auc = 2
    self.exec_performance = self.exec_accuracy
    self.normalize_performance = True

    ################################### IRT ####################################
    #execute theta ou trueScore
    self.exec_theta = 0
    self.exec_trueScore = 1
    self.exec_base_irt_score = self.exec_trueScore

    # calculo de  theta
    self.theta_sum = 0
    self.theta_min = 1
    self.theta_mean = 2
    self.exec_calc_theta = self.theta_mean


    # irt algorithm ‘ternary’, ‘dichotomous’, ‘fibonacci’, ‘golden’, ‘brent’, ‘bounded’ and ‘golden2’
    self.irt_method_fibonacci = '-metodo fibonacci'
    self.irt_method_bounded = '-metodo bounded'
    self.irt_method_ternary = '-metodo ternary' #long time execution
    self.irt_method_dichotomous = '-metodo dichotomous' #long time execution
    self.irt_method_golden = '-metodo golden'
    self.irt_method_brent = '-metodo brent'
    self.irt_method_golden2 = '-metodo golden2' #problem in execution
    self.irt_method = self.irt_method_bounded

    # Properties of IRT
    self.irt_discriminate = True #False remove the property by IRTs calc.
    self.irt_difficulty = True #False remove the property by IRTs calc.
    self.irt_divine = True #False remove the property by IRTs calc.

    ################################## PROPOSAL 1 POOL #########################
    self.include_original_clf_data_pool = True
    self.number_of_features_deletion = 1 # values 1 to ++

    self.list_clf_pool = [] #empity

    ################################## PROPOSAL 2 LOOP #########################

    self.include_original_clf_data_loop = True
    self.number_of_features_variation = 1 # values 1 to 4

    # test or train
    self.exec_test = 0
    self.exec_train = 1
    self.exec_in = self.exec_test

    #loop of models variation
    self.exec_permutation = 0 # random base
    self.exec_noise = 1 # random base
    self.exec_zeros = 2
    self.exec_norm = 3 
    self.exec_ordup = 4
    self.exec_orddown = 5
    self.exec_inver = 6
    self.exec_binning = 7
    self.exec_mult_neg = 8
    self.exec_mean = 9
    self.exec_std = 10
    self.exec_zscore = 11
    self.exec_variation_method = [self.exec_mult_neg, self.exec_binning, self.exec_zeros, self.exec_ordup, self.exec_inver, self.exec_std, self.exec_zscore]

    #list of thetas
    self.list_clf_loop = [] #empity

  ########################## Global declaration ################################

  def z_score_serie(self, s):
    # copy the dataframe
    s_std = s.copy()
    s_std = (s_std - s_std.mean()) / s_std.std()
    return s_std

  def auc_score(self, y, y_pred):
      
      fpr, tpr, thresholds = metrics.roc_curve(y, y_pred, pos_label=2)
      
      return metrics.auc(fpr, tpr)

  def powerSetLimited(self, s,l):

      def powerset(s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]
      
      psl = []
      ps = list(powerset(s))
      for _,i in enumerate(ps):
        if len(i) <= l and len(i)>0:
          psl.append(i)
      return psl

  def run_prepare(self, model,data_exec_x, data_exec_y, X_train, X_test, y_train, y_test,model_name):
    if os.path.isfile(self.path_content+self.path_irt+self.bar+'tabela_base_para_executar_irt_'+model_name+'.csv'):
        os.remove(self.path_content+self.path_irt+self.bar+'tabela_base_para_executar_irt_'+model_name+'.csv')
    if os.path.isfile(self.path_content+self.path_irt+self.bar+'tabela_base_para_executar_irt_accuracy_'+model_name+'.csv'):
        os.remove(self.path_content+self.path_irt+self.bar+'tabela_base_para_executar_irt_accuracy_'+model_name+'.csv')

    def compResponses(a,b):
      c = []
      for i,_ in enumerate(a):
        if a[i] == b[i]:
          c.append(1)
        else:
          c.append(0)
      return c    

    #Prediction
    original_outputs = model.predict(data_exec_x)


    #XAI-IRT
    # train, test, model and outputs

    #Loop of models
    df_loop_of_models = pd.DataFrame()
    
    #Prepare df_loop_of_models
    #df_loop_of_models['Clf'] = [] 
    #for i in range(len(data_exec_y)):
    #  df_loop_of_models['V'+str(i)] = []
    
    list_col_tmp = ['Clf']
    for i in range(len(data_exec_y)):
      list_col_tmp.append('V'+str(i))
    df_loop_of_models = pd.DataFrame(columns=list_col_tmp)

    df_loop_of_models_performance = pd.DataFrame(columns=['Metodo','Acuracia'])



    if self.exec_proposal == self.proposal_2_loop:
      if self.verbose:
        print('Original data')
        print(data_exec_x)

      number_of_instances = len(data_exec_x)

      if self.include_original_clf_data_loop:
        str_tmp = 'Clf original data'
        if self.exec_performance == self.exec_accuracy:
          result_accuracy = accuracy_score(y_true = original_outputs, y_pred = original_outputs, normalize=self.normalize_performance) #accuracy
        else:
          if self.exec_performance == self.exec_auc:
            result_accuracy = self.auc_score(original_outputs, original_outputs) #AUC

        result_bin = compResponses(list(original_outputs), list(original_outputs))
        result_bin.insert(0,str_tmp)
        df_loop_of_models.loc[len(df_loop_of_models)] = result_bin
        df_loop_of_models_performance.loc[len(df_loop_of_models_performance)] = [str_tmp, result_accuracy] 
      
      #inset variation of ONE attribute in loop of models
      if self.number_of_features_variation >= 1:
        for _, variation in enumerate(self.exec_variation_method):
          for id,c in enumerate(data_exec_x.columns):
            #criando cópia do dado inicial
            data_exec_x_copy = data_exec_x.copy()
            if variation == self.exec_permutation:
              #trocando posições de cada instância do atributo da vez
              random_id = random.sample(range(0,number_of_instances), number_of_instances)
              data_exec_x_copy[c] = data_exec_x_copy[c].values[random_id]
              method = 'Permutation'
            else:
              if variation == self.exec_noise:
                #aplica ruido a cada instâcia do atributo da vez
                noise = np.random.normal(0, 1, number_of_instances)
                data_exec_x_copy[c] = data_exec_x_copy[c] + noise
                method = 'Noise'
              else: 
                if variation == self.exec_zeros:
                  #aplica zeros a cada instância do atributo da vez
                  zeros = np.zeros(number_of_instances)
                  data_exec_x_copy[c] = zeros
                  method = 'Zeros'
                else:
                  if variation == self.exec_norm:
                    #normaliza os elementos
                    norm = np.linalg.norm(data_exec_x_copy[c])
                    normal_array = data_exec_x_copy[c]/norm
                    data_exec_x_copy[c] = normal_array
                    method = 'Normalization'
                  else:
                    if variation == self.exec_ordup:
                      #ordena em ordem crescente os elementos
                      order_up = np.sort(data_exec_x_copy[c])
                      data_exec_x_copy[c] = order_up
                      method = 'Ordernation_Up'
                    else:
                      if variation == self.exec_orddown:
                        #ordena em ordem decrescente os elementos
                        order_down = -np.sort(-data_exec_x_copy[c])
                        data_exec_x_copy[c] = order_down
                        method = 'Ordernation_Down'
                      else:
                        if variation == self.exec_inver:
                          #inverte os elementos
                          transp = np.flipud(data_exec_x_copy[c])
                          data_exec_x_copy[c] = transp
                          method = 'Invertion'
                        else:
                          if variation == self.exec_binning:
                            #inverte os elementos
                            mean_arr = np.mean(data_exec_x_copy[c])
                            binn = np.digitize(data_exec_x_copy[c],bins=[mean_arr])
                            data_exec_x_copy[c] = binn
                            method = 'Binning'
                          else:
                            if variation == self.exec_mult_neg:
                              #multiplica por -1
                              data_exec_x_copy[c] = data_exec_x_copy[c] * -1
                              method = 'MultNeg'
                            else:
                              if variation == self.exec_mean:
                                #mean
                                inst =  len(data_exec_x_copy[c])
                                data_exec_x_copy[c] = [statistics.mean(data_exec_x_copy[c])]*inst
                                method = 'Mean'
                              else:
                                if variation == self.exec_std:
                                  #std
                                  inst =  len(data_exec_x_copy[c])
                                  data_exec_x_copy[c] = [statistics.stdev(data_exec_x_copy[c])]*inst
                                  method = 'Std'
                                else:
                                  if variation == self.exec_zscore:
                                    #zscore
                                    data_exec_x_copy[c] = self.z_score_serie(data_exec_x_copy[c])
                                    method = 'Zscore'

            if self.verbose:
              print('')
              print(method,' of ',c)
              print(data_exec_x_copy)
            if self.verbose_graph:
              data_exec_x_copy.plot.kde(by=data_exec_x_copy.columns, alpha=0.5,title=str(method+' of '+c))

            data_exec_x_copy = data_exec_x_copy.fillna(0) # fix nan or infinity
            
            result_pred = model.predict(data_exec_x_copy) #prediction

            if self.exec_performance == self.exec_accuracy:
              result_accuracy = accuracy_score(y_true = original_outputs, y_pred = result_pred, normalize=self.normalize_performance) #accuracy
            else:
              if self.exec_performance == self.exec_auc:
                result_accuracy = self.auc_score(original_outputs, result_pred) #AUC

            
            str_model_name = 'Clf '+method+' "'+str(c)+'"'
            self.list_clf_loop.append(str_model_name)
            result_bin = compResponses(list(original_outputs), list(result_pred))
            result_bin.insert(0,str_model_name)
            df_loop_of_models.loc[len(df_loop_of_models)] = result_bin
            df_loop_of_models_performance.loc[len(df_loop_of_models_performance)] = [str_model_name, result_accuracy]

      #inset invertion of TWO attributes in loop of models
      if self.number_of_features_variation >= 2:
        for _,variation in enumerate(self.exec_variation_method):
          for id1,c1 in enumerate(data_exec_x.columns):
            for id2,c2 in enumerate(data_exec_x.columns):
              if id2 > id1:
                #criando cópia do dado inicial
                data_exec_x_copy = data_exec_x.copy()
                if variation == self.exec_permutation:
                  #trocando posições de cada instância do atributo da vez
                  random_id = random.sample(range(0,number_of_instances), number_of_instances)
                  data_exec_x_copy[c1] = data_exec_x_copy[c1].values[random_id]
                  random_id = random.sample(range(0,number_of_instances), number_of_instances)
                  data_exec_x_copy[c2] = data_exec_x_copy[c2].values[random_id]
                  method = 'Permutation'
                else:
                  if variation == self.exec_noise:
                    #aplica ruido a cada instâcia do atributo da vez
                    noise = np.random.normal(0, 1, number_of_instances)
                    data_exec_x_copy[c1] = data_exec_x_copy[c1] + noise
                    noise = np.random.normal(0, 1, number_of_instances)
                    data_exec_x_copy[c2] = data_exec_x_copy[c2] + noise
                    method = 'Noise'
                  else:
                    if variation == self.exec_zeros:
                      #aplica zeros a cada instância do atributo da vez
                      zeros = np.zeros(number_of_instances)
                      data_exec_x_copy[c1] = zeros
                      data_exec_x_copy[c2] = zeros
                      method = 'Zeros'
                    else:
                      if variation == self.exec_norm:
                        #normaliza os elementos
                        norm = np.linalg.norm(data_exec_x_copy[c1])
                        normal_array = data_exec_x_copy[c1]/norm
                        data_exec_x_copy[c1] = normal_array
                        norm = np.linalg.norm(data_exec_x_copy[c2])
                        normal_array = data_exec_x_copy[c2]/norm
                        data_exec_x_copy[c2] = normal_array
                        method = 'Normalization'
                      else:
                        if variation == self.exec_ordup:
                          #ordena em ordem crescente os elementos
                          order_up = np.sort(data_exec_x_copy[c1])
                          data_exec_x_copy[c1] = order_up
                          order_up = np.sort(data_exec_x_copy[c2])
                          data_exec_x_copy[c2] = order_up
                          method = 'Ordernation_Up'
                        else:
                          if variation == self.exec_orddown:
                            #ordena em ordem decrescente os elementos
                            order_down = -np.sort(-data_exec_x_copy[c1])
                            data_exec_x_copy[c1] = order_down
                            order_down = -np.sort(-data_exec_x_copy[c2])
                            data_exec_x_copy[c2] = order_down
                            method = 'Ordernation_Down'
                          else:
                            if variation == self.exec_inver:
                              #inverte os elementos
                              transp = np.flipud(data_exec_x_copy[c1])
                              data_exec_x_copy[c1] = transp
                              transp = np.flipud(data_exec_x_copy[c2])
                              data_exec_x_copy[c2] = transp
                              method = 'Invertion'
                            else:
                              if variation == self.exec_binning:
                                #inverte os elementos
                                mean_arr = np.mean(data_exec_x_copy[c1])
                                binn = np.digitize(data_exec_x_copy[c1],bins=[mean_arr])
                                data_exec_x_copy[c1] = binn
                                mean_arr = np.mean(data_exec_x_copy[c2])
                                binn = np.digitize(data_exec_x_copy[c2],bins=[mean_arr])
                                data_exec_x_copy[c2] = binn
                                method = 'Binning'
                              else:
                                if variation == self.exec_mult_neg:
                                  #multiplica por -1
                                  data_exec_x_copy[c1] = data_exec_x_copy[c1] * -1
                                  data_exec_x_copy[c2] = data_exec_x_copy[c2] * -1
                                  method = 'MultNeg'
                                else:
                                  if variation == self.exec_mean:
                                    #mean
                                    inst =  len(data_exec_x_copy[c1])
                                    data_exec_x_copy[c1] = [statistics.mean(data_exec_x_copy[c1])]*inst
                                    data_exec_x_copy[c2] = [statistics.mean(data_exec_x_copy[c2])]*inst
                                    method = 'Mean'
                                  else:
                                    if variation == self.exec_std:
                                      #std
                                      inst =  len(data_exec_x_copy[c1])
                                      data_exec_x_copy[c1] = [statistics.stdev(data_exec_x_copy[c1])]*inst
                                      data_exec_x_copy[c2] = [statistics.stdev(data_exec_x_copy[c2])]*inst
                                      method = 'Std'
                                    else:
                                      if variation == self.exec_zscore:
                                        #zscore
                                        data_exec_x_copy[c1] = self.z_score_serie(data_exec_x_copy[c1])
                                        data_exec_x_copy[c2] = self.z_score_serie(data_exec_x_copy[c2])
                                        method = 'Zscore'

                str_model_name = 'Clf '+method+' "'+str(c1)+'" and "'+str(c2)+'"'
                if self.verbose:
                  print('')
                  print(str_model_name)
                  print(data_exec_x_copy)
                if self.verbose_graph:
                  data_exec_x_copy.plot.kde(by=data_exec_x_copy.columns, alpha=0.5,title=str_model_name)

                data_exec_x_copy = data_exec_x_copy.fillna(0) # fix nan or infinity
                
                #executando o modelo com o atributo da vez embaralhado
                result_pred = model.predict(data_exec_x_copy) #prediction

                if self.exec_performance == self.exec_accuracy:
                  result_accuracy = accuracy_score(y_true = original_outputs, y_pred = result_pred, normalize=self.normalize_performance) #accuracy
                else:
                  if self.exec_performance == self.exec_auc:
                    result_accuracy = self.auc_score(original_outputs, result_pred) #AUC

               
                str_model_name = 'Clf '+method+' "'+str(c1)+'" and "'+str(c2)+'"'
                self.list_clf_loop.append(str_model_name)
                result_bin = compResponses(list(original_outputs), list(result_pred))
                result_bin.insert(0,str_model_name)
                df_loop_of_models.loc[len(df_loop_of_models)] = result_bin
                df_loop_of_models_performance.loc[len(df_loop_of_models_performance)] = [str_model_name, result_accuracy]
              else:
                pass

      #inset invertion of Three attributes in loop of models
      if self.number_of_features_variation >= 3:
        for _, variation in enumerate(self.exec_variation_method):
          for id1,c1 in enumerate(data_exec_x.columns):
            for id2,c2 in enumerate(data_exec_x.columns):
              for id3,c3 in enumerate(data_exec_x.columns):
                if id3 > id2 and id2 > id1:
                  #criando cópia do dado inicial
                  data_exec_x_copy = data_exec_x.copy()
                  if variation == self.exec_permutation:
                    #trocando posições de cada instância do atributo da vez
                    random_id = random.sample(range(0,number_of_instances), number_of_instances)
                    data_exec_x_copy[c1] = data_exec_x_copy[c1].values[random_id]
                    random_id = random.sample(range(0,number_of_instances), number_of_instances)
                    data_exec_x_copy[c2] = data_exec_x_copy[c2].values[random_id]
                    random_id = random.sample(range(0,number_of_instances), number_of_instances)
                    data_exec_x_copy[c3] = data_exec_x_copy[c3].values[random_id]
                    method = 'Permutation'
                  else:
                    if variation == self.exec_noise:
                      #aplica ruido a cada instâcia do atributo da vez
                      noise = np.random.normal(0, 1, number_of_instances)
                      data_exec_x_copy[c1] = data_exec_x_copy[c1] + noise
                      noise = np.random.normal(0, 1, number_of_instances)
                      data_exec_x_copy[c2] = data_exec_x_copy[c2] + noise
                      noise = np.random.normal(0, 1, number_of_instances)
                      data_exec_x_copy[c3] = data_exec_x_copy[c3] + noise
                      method = 'Noise'
                    else:
                      if variation == self.exec_zeros:
                        #aplica zeros a cada instância do atributo da vez
                        zeros = np.zeros(number_of_instances)
                        data_exec_x_copy[c1] = zeros
                        data_exec_x_copy[c2] = zeros
                        data_exec_x_copy[c3] = zeros
                        method = 'Zeros'
                      else:
                        if variation == self.exec_norm:
                          #normaliza os elementos
                          norm = np.linalg.norm(data_exec_x_copy[c1])
                          normal_array = data_exec_x_copy[c1]/norm
                          data_exec_x_copy[c1] = normal_array
                          norm = np.linalg.norm(data_exec_x_copy[c2])
                          normal_array = data_exec_x_copy[c2]/norm
                          data_exec_x_copy[c2] = normal_array
                          normal_array = data_exec_x_copy[c3]/norm
                          data_exec_x_copy[c3] = normal_array
                          method = 'Normalization'
                        else:
                          if variation == self.exec_ordup:
                            #ordena em ordem crescente os elementos
                            order_up = np.sort(data_exec_x_copy[c1])
                            data_exec_x_copy[c1] = order_up
                            order_up = np.sort(data_exec_x_copy[c2])
                            data_exec_x_copy[c2] = order_up
                            order_up = np.sort(data_exec_x_copy[c3])
                            data_exec_x_copy[c3] = order_up
                            method = 'Ordernation_Up'
                          else:
                            if variation == self.exec_orddown:
                              #ordena em ordem decrescente os elementos
                              order_down = -np.sort(-data_exec_x_copy[c1])
                              data_exec_x_copy[c1] = order_down
                              order_down = -np.sort(-data_exec_x_copy[c2])
                              data_exec_x_copy[c2] = order_down
                              order_down = -np.sort(-data_exec_x_copy[c3])
                              data_exec_x_copy[c3] = order_down
                              method = 'Ordernation_Down'
                            else:
                              if variation == self.exec_inver:
                                #inverte os elementos
                                transp = np.flipud(data_exec_x_copy[c1])
                                data_exec_x_copy[c1] = transp
                                transp = np.flipud(data_exec_x_copy[c2])
                                data_exec_x_copy[c2] = transp
                                transp = np.flipud(data_exec_x_copy[c3])
                                data_exec_x_copy[c3] = transp
                                method = 'Invertion'
                              else:
                                if variation == self.exec_binning:
                                  #inverte os elementos
                                  mean_arr = np.mean(data_exec_x_copy[c1])
                                  binn = np.digitize(data_exec_x_copy[c1],bins=[mean_arr])
                                  data_exec_x_copy[c1] = binn
                                  mean_arr = np.mean(data_exec_x_copy[c2])
                                  binn = np.digitize(data_exec_x_copy[c2],bins=[mean_arr])
                                  data_exec_x_copy[c2] = binn
                                  mean_arr = np.mean(data_exec_x_copy[c3])
                                  binn = np.digitize(data_exec_x_copy[c3],bins=[mean_arr])
                                  data_exec_x_copy[c3] = binn
                                  method = 'Binning'
                                else:
                                  if variation == self.exec_mult_neg:
                                    #multiplica por -1
                                    data_exec_x_copy[c1] = data_exec_x_copy[c1] * -1
                                    data_exec_x_copy[c2] = data_exec_x_copy[c2] * -1
                                    data_exec_x_copy[c3] = data_exec_x_copy[c3] * -1
                                    method = 'MultNeg'
                                  else:
                                    if variation == self.exec_mean:
                                      #mean
                                      inst =  len(data_exec_x_copy[c1])
                                      data_exec_x_copy[c1] = [statistics.mean(data_exec_x_copy[c1])]*inst
                                      data_exec_x_copy[c2] = [statistics.mean(data_exec_x_copy[c2])]*inst
                                      data_exec_x_copy[c3] = [statistics.mean(data_exec_x_copy[c3])]*inst
                                      method = 'Mean'
                                    else:
                                      if variation == self.exec_std:
                                        #std
                                        inst =  len(data_exec_x_copy[c1])
                                        data_exec_x_copy[c1] = [statistics.stdev(data_exec_x_copy[c1])]*inst
                                        data_exec_x_copy[c2] = [statistics.stdev(data_exec_x_copy[c2])]*inst
                                        data_exec_x_copy[c3] = [statistics.stdev(data_exec_x_copy[c3])]*inst
                                        method = 'Std'
                                      else:
                                        if variation == self.exec_zscore:
                                          #zscore
                                          data_exec_x_copy[c1] = self.z_score_serie(data_exec_x_copy[c1])
                                          data_exec_x_copy[c2] = self.z_score_serie(data_exec_x_copy[c2])
                                          data_exec_x_copy[c3] = self.z_score_serie(data_exec_x_copy[c3])
                                          method = 'Zscore'

                    
                  str_model_name = 'Clf '+method+' "'+str(c1)+'" and "'+str(c2)+'" and "'+str(c3)+'"'
                  if self.verbose:
                    print('')
                    print(str_model_name)
                    print(data_exec_x_copy)
                  if self.verbose_graph:
                    data_exec_x_copy.plot.kde(by=data_exec_x_copy.columns, alpha=0.5,title=str_model_name)

                  data_exec_x_copy = data_exec_x_copy.fillna(0) # fix nan or infinity
                  result_pred = model.predict(data_exec_x_copy) #prediction

                  if self.exec_performance == self.exec_accuracy:
                    result_accuracy = accuracy_score(y_true = original_outputs, y_pred = result_pred, normalize=self.normalize_performance) #accuracy
                  else:
                    if self.exec_performance == self.exec_auc:
                      result_accuracy = self.auc_score(original_outputs, result_pred) #AUC

                  
                  self.list_clf_loop.append(str_model_name)
                  result_bin = compResponses(list(original_outputs), list(result_pred))
                  result_bin.insert(0,str_model_name)
                  df_loop_of_models.loc[len(df_loop_of_models)] = result_bin
                  df_loop_of_models_performance.loc[len(df_loop_of_models_performance)] = [str_model_name, result_accuracy]
                else:
                  pass

      #inset invertion of Four attributes in loop of models
      if self.number_of_features_variation == 4:
        for _, variation in enumerate(self.exec_variation_method):
          for id1,c1 in enumerate(data_exec_x.columns):
            for id2,c2 in enumerate(data_exec_x.columns):
              for id3,c3 in enumerate(data_exec_x.columns):
                for id4,c4 in enumerate(data_exec_x.columns):
                  if id4 > id3 and id3 > id2 and id2 > id1:
                    #criando cópia do dado inicial
                    data_exec_x_copy = data_exec_x.copy()
                    if variation == self.exec_permutation:
                      #trocando posições de cada instância do atributo da vez
                      random_id = random.sample(range(0,number_of_instances), number_of_instances)
                      data_exec_x_copy[c1] = data_exec_x_copy[c1].values[random_id]
                      random_id = random.sample(range(0,number_of_instances), number_of_instances)
                      data_exec_x_copy[c2] = data_exec_x_copy[c2].values[random_id]
                      random_id = random.sample(range(0,number_of_instances), number_of_instances)
                      data_exec_x_copy[c3] = data_exec_x_copy[c3].values[random_id]
                      random_id = random.sample(range(0,number_of_instances), number_of_instances)
                      data_exec_x_copy[c4] = data_exec_x_copy[c4].values[random_id]
                      method = 'Permutation'
                    else:
                      if variation == self.exec_noise:
                        #aplica ruido a cada instâcia do atributo da vez
                        noise = np.random.normal(0, 1, number_of_instances)
                        data_exec_x_copy[c1] = data_exec_x_copy[c1] + noise
                        noise = np.random.normal(0, 1, number_of_instances)
                        data_exec_x_copy[c2] = data_exec_x_copy[c2] + noise
                        noise = np.random.normal(0, 1, number_of_instances)
                        data_exec_x_copy[c3] = data_exec_x_copy[c3] + noise
                        noise = np.random.normal(0, 1, number_of_instances)
                        data_exec_x_copy[c4] = data_exec_x_copy[c4] + noise
                        method = 'Noise'
                      else:
                        if variation == self.exec_zeros:
                          #aplica zeros a cada instância do atributo da vez
                          zeros = np.zeros(number_of_instances)
                          data_exec_x_copy[c1] = zeros
                          data_exec_x_copy[c2] = zeros
                          data_exec_x_copy[c3] = zeros
                          data_exec_x_copy[c4] = zeros
                          method = 'Zeros'
                        else:
                          if variation == self.exec_norm:
                            #normaliza os elementos
                            norm = np.linalg.norm(data_exec_x_copy[c1])
                            normal_array = data_exec_x_copy[c1]/norm
                            data_exec_x_copy[c1] = normal_array
                            norm = np.linalg.norm(data_exec_x_copy[c2])
                            normal_array = data_exec_x_copy[c2]/norm
                            data_exec_x_copy[c2] = normal_array
                            normal_array = data_exec_x_copy[c3]/norm
                            data_exec_x_copy[c3] = normal_array
                            normal_array = data_exec_x_copy[c4]/norm
                            data_exec_x_copy[c4] = normal_array
                            method = 'Normalization'
                          else:
                            if variation == self.exec_ordup:
                              #ordena em ordem crescente os elementos
                              order_up = np.sort(data_exec_x_copy[c1])
                              data_exec_x_copy[c1] = order_up
                              order_up = np.sort(data_exec_x_copy[c2])
                              data_exec_x_copy[c2] = order_up
                              order_up = np.sort(data_exec_x_copy[c3])
                              data_exec_x_copy[c3] = order_up
                              order_up = np.sort(data_exec_x_copy[c4])
                              data_exec_x_copy[c4] = order_up
                              method = 'Ordernation_Up'
                            else:
                              if variation == self.exec_orddown:
                                #ordena em ordem decrescente os elementos
                                order_down = -np.sort(-data_exec_x_copy[c1])
                                data_exec_x_copy[c1] = order_down
                                order_down = -np.sort(-data_exec_x_copy[c2])
                                data_exec_x_copy[c2] = order_down
                                order_down = -np.sort(-data_exec_x_copy[c3])
                                data_exec_x_copy[c3] = order_down
                                order_down = -np.sort(-data_exec_x_copy[c4])
                                data_exec_x_copy[c4] = order_down
                                method = 'Ordernation_Down'
                              else:
                                if variation == self.exec_inver:
                                  #inverte os elementos
                                  transp = np.flipud(data_exec_x_copy[c1])
                                  data_exec_x_copy[c1] = transp
                                  transp = np.flipud(data_exec_x_copy[c2])
                                  data_exec_x_copy[c2] = transp
                                  transp = np.flipud(data_exec_x_copy[c3])
                                  data_exec_x_copy[c3] = transp
                                  transp = np.flipud(data_exec_x_copy[c4])
                                  data_exec_x_copy[c4] = transp
                                  method = 'Invertion'
                                else:
                                  if variation == self.exec_binning:
                                    #inverte os elementos
                                    mean_arr = np.mean(data_exec_x_copy[c1])
                                    binn = np.digitize(data_exec_x_copy[c1],bins=[mean_arr])
                                    data_exec_x_copy[c1] = binn
                                    mean_arr = np.mean(data_exec_x_copy[c2])
                                    binn = np.digitize(data_exec_x_copy[c2],bins=[mean_arr])
                                    data_exec_x_copy[c2] = binn
                                    mean_arr = np.mean(data_exec_x_copy[c3])
                                    binn = np.digitize(data_exec_x_copy[c3],bins=[mean_arr])
                                    data_exec_x_copy[c3] = binn
                                    mean_arr = np.mean(data_exec_x_copy[c4])
                                    binn = np.digitize(data_exec_x_copy[c4],bins=[mean_arr])
                                    data_exec_x_copy[c4] = binn
                                    method = 'Binning'
                                  else:
                                    if variation == self.exec_mult_neg:
                                      #multiplica por -1
                                      data_exec_x_copy[c1] = data_exec_x_copy[c1] * -1
                                      data_exec_x_copy[c2] = data_exec_x_copy[c2] * -1
                                      data_exec_x_copy[c3] = data_exec_x_copy[c3] * -1
                                      data_exec_x_copy[c4] = data_exec_x_copy[c4] * -1
                                      method = 'MultNeg'
                                    else:
                                      if variation == self.exec_mean:
                                        #mean
                                        inst =  len(data_exec_x_copy[c1])
                                        data_exec_x_copy[c1] = [statistics.mean(data_exec_x_copy[c1])]*inst
                                        data_exec_x_copy[c2] = [statistics.mean(data_exec_x_copy[c2])]*inst
                                        data_exec_x_copy[c3] = [statistics.mean(data_exec_x_copy[c3])]*inst
                                        data_exec_x_copy[c4] = [statistics.mean(data_exec_x_copy[c4])]*inst
                                        method = 'Mean'
                                      else:
                                        if variation == self.exec_std:
                                          #std
                                          inst =  len(data_exec_x_copy[c1])
                                          data_exec_x_copy[c1] = [statistics.stdev(data_exec_x_copy[c1])]*inst
                                          data_exec_x_copy[c2] = [statistics.stdev(data_exec_x_copy[c2])]*inst
                                          data_exec_x_copy[c3] = [statistics.stdev(data_exec_x_copy[c3])]*inst
                                          data_exec_x_copy[c4] = [statistics.stdev(data_exec_x_copy[c4])]*inst
                                          method = 'Std'
                                        else:
                                          if variation == self.exec_zscore:
                                            #zscore
                                            data_exec_x_copy[c1] = self.z_score_serie(data_exec_x_copy[c1])
                                            data_exec_x_copy[c2] = self.z_score_serie(data_exec_x_copy[c2])
                                            data_exec_x_copy[c3] = self.z_score_serie(data_exec_x_copy[c3])
                                            data_exec_x_copy[c4] = self.z_score_serie(data_exec_x_copy[c4])
                                            method = 'Zscore'
                    
                    str_model_name = 'Clf '+method+' "'+str(c1)+'" and "'+str(c2)+'" and "'+str(c3)+'" and "'+str(c4)+'"'
                    if self.verbose:
                      print('')
                      print(str_model_name)
                      print(data_exec_x_copy)
                    if self.verbose_graph:
                      data_exec_x_copy.plot.kde(by=data_exec_x_copy.columns, alpha=0.5,title=str_model_name)
                    
                    data_exec_x_copy = data_exec_x_copy.fillna(0) # fix nan or infinity      
                    result_pred = model.predict(data_exec_x_copy) #prediction

                    if self.exec_performance == self.exec_accuracy:
                      result_accuracy = accuracy_score(y_true = original_outputs, y_pred = result_pred, normalize=self.normalize_performance) #accuracy
                    else:
                      if self.exec_performance == self.exec_auc:
                        result_accuracy = self.auc_score(original_outputs, result_pred) #AUC

                    
                    self.list_clf_loop.append(str_model_name)
                    result_bin = compResponses(list(original_outputs), list(result_pred))
                    result_bin.insert(0,str_model_name)
                    df_loop_of_models.loc[len(df_loop_of_models)] = result_bin
                    df_loop_of_models_performance.loc[len(df_loop_of_models_performance)] = [str_model_name, result_accuracy]
                  else:
                    pass
    else:
      if self.exec_proposal == self.proposal_1_pool:
        
        model_copy = copy.deepcopy(model)
        

        if self.include_original_clf_data_pool:
          original_outputs = model_copy.predict(X_test)
          
          if self.exec_performance == self.exec_accuracy:
            result_accuracy = accuracy_score(y_true = original_outputs, y_pred = original_outputs, normalize=self.normalize_performance) #accuracy
          else:
            if self.exec_performance == self.exec_auc:
              result_accuracy = self.auc_score(original_outputs, original_outputs) #AUC
          
          result_pred = (original_outputs == original_outputs) #binarization
          

          str_model_name = 'Original model'
          self.list_clf_pool.append(str_model_name)
          df_loop_of_models.loc[len(df_loop_of_models)] = result_pred.astype(int)[:].tolist().insert(0,str_model_name) #boolean to int
          df_loop_of_models_performance.loc[len(df_loop_of_models_performance)] = [str_model_name, result_accuracy]
          if self.verbose:
            print('')
            print(str_model_name)
            print(X_test)
        
        ps = self.powerSetLimited(data_exec_x.columns, self.number_of_features_deletion) #powerset of all features
        
        for _, ps_c in enumerate(ps):
          data_train_x_copy = X_train.copy()
          data_test_x_copy = X_test.copy()
          for _, c in enumerate(ps_c):
            flag_none = True
            #remove feature c
            data_train_x_copy = data_train_x_copy.drop(c, axis='columns')
            data_test_x_copy = data_test_x_copy.drop(c, axis='columns')

          if len(data_train_x_copy.columns) == 0:
            break

          #train new model
          model_copy.fit(data_train_x_copy, y_train)

          result_pred = model_copy.predict(data_test_x_copy)
          if self.exec_performance == self.exec_accuracy:
            result_accuracy = accuracy_score(y_true = original_outputs, y_pred = result_pred, normalize=self.normalize_performance) #accuracy
          else:
            if self.exec_performance == self.exec_auc:
              result_accuracy = self.auc_score(original_outputs, result_pred) #AUC

          
            
          str_model_name = 'Clf feature elimination: '
          for _, i in enumerate(ps_c):
            str_model_name = str_model_name + '"'+str(i)+'" '
          self.list_clf_pool.append(str_model_name)
          result_bin = compResponses(list(original_outputs), list(result_pred))
          result_bin.insert(0,str_model_name)
          df_loop_of_models.loc[len(df_loop_of_models)] = result_bin
          df_loop_of_models_performance.loc[len(df_loop_of_models_performance)] = [str_model_name, result_accuracy]
          if self.verbose:
            print('')
            print(str_model_name)
            print(data_test_x_copy)

    df_loop_of_models = df_loop_of_models.set_index('Clf')
    if self.verbose:
      print('Resume Loop of model')
      print(df_loop_of_models)
      print()
      print('Resume Loop of model accuracy')
      print(df_loop_of_models_performance)

    df = df_loop_of_models
    df.to_csv(self.path_content+self.path_irt+self.bar+"tabela_base_para_executar_irt_"+model_name+".csv",',')
    #if self.download_files:
    #  files.download(self.path_content+self.path_irt+self.bar+"tabela_base_para_executar_irt.csv") 

    df = df_loop_of_models_performance
    df.to_csv(self.path_content+self.path_irt+self.bar+"tabela_base_para_executar_irt_accuracy_"+model_name+".csv",',',index=False)
    #if self.download_files:
    #  files.download(self.path_content+self.path_irt+self.bar+"tabela_base_para_executar_irt_accuracy.csv")

    return  df_loop_of_models, df_loop_of_models_performance

  def run_irt(self, datasetName,model_name):

    if os.path.isfile(self.path_content+self.path_irt+self.bar+'irt_item_param.csv'):
        os.remove(self.path_content+self.path_irt+self.bar+'irt_item_param.csv')
    if os.path.isfile(self.path_content+self.path_irt+self.bar+'irt_item_param_new_'+model_name+'.csv'):
        os.remove(self.path_content+self.path_irt+self.bar+'irt_item_param_new_'+model_name+'.csv')
    if os.path.isfile(self.path_content+self.path_irt+self.bar+'OutExecution'+self.bar+'theta_list_'+model_name+'.csv'):
        os.remove(self.path_content+self.path_irt+self.bar+'OutExecution'+self.bar+'theta_list_'+model_name+'.csv')
    if os.path.isfile(self.path_content+self.path_irt+self.bar+'OutExecution'+self.bar+'score_total_'+model_name+'.csv'):
        os.remove(self.path_content+self.path_irt+self.bar+'OutExecution'+self.bar+'score_total_'+model_name+'.csv')
    
    try:
        #!python decodIRT_MLtIRT.py -dir $self.path_content_simple+self.path_irt -respMatrix $self.path_content$self.path_irt$self.bar'tabela_base_para_executar_irt.csv'
        os.system('python decodIRT_MLtIRT.py -dir ' + self.path_content_simple+self.path_irt + ' -respMatrix ' + self.path_content+self.path_irt+self.bar+'tabela_base_para_executar_irt_'+model_name+'.csv')
    except Exception as error:
      # handle the exception
      print("Erro ocorreu no eXirt (execução do decodIRT_MLtIRT):", error)
    

    result_irt = pd.read_csv(self.path_content+self.path_irt+self.bar+'irt_item_param.csv')
    
    
    result_irt_new = result_irt.copy()

    #save parameters of item by datset
    result_irt_dataset = result_irt.copy()
    result_irt_dataset.to_csv(self.path_content+self.path_irt+self.path_dataset+self.bar+'irt_item_param_'+datasetName+'_'+model_name+'.csv',index=False)
    path_item_param = self.path_content+self.path_irt+self.path_dataset+self.bar+'irt_item_param_'+datasetName+'_'+model_name+'.csv'
    path_out_plt = self.path_content+self.path_fig+self.path_dataset+self.bar+'irt_item_param_'+datasetName+'_'+model_name+'_icc.png' 
    plotICC(path_item_param, path_out_plt, 'ICC: '+datasetName) 

    if self.irt_divine == False:
      result_irt_new['Adivinhacao'] = [0]*len(result_irt_new['Adivinhacao']) #anula os valores de adivinhação
    if self.irt_difficulty == False:
      result_irt_new['Dificuldade'] = [0]*len(result_irt_new['Dificuldade']) #anula os valores de dificuldade
    if self.irt_discriminate == False:
      result_irt_new['Discriminacao'] = [0]*len(result_irt_new['Discriminacao']) #anula os valores de Discriminacao

    result_irt_new.to_csv(self.path_content+self.path_irt+self.bar+'irt_item_param_new_'+model_name+'.csv',index=False)

    try:
      os.system('python decodIRT_analysis.py -dir ' + self.path_content_simple+self.path_irt + ' -nameData '+self.bar+'OutExecution -respMatrix ' + self.path_content+self.path_irt+self.bar+'tabela_base_para_executar_irt_'+model_name+'.csv -IRTparam '+self.path_content+self.path_irt+self.bar+'irt_item_param_new_'+model_name+'.csv -accur '+self.path_content+self.path_irt+self.bar+'tabela_base_para_executar_irt_accuracy_'+model_name+'.csv -scoreAll -save ' + self.irt_method + ' -missing')
    except Exception as error:
      # handle the exception
      print("Erro ocorreu no eXirt (execução do decodIRT_analysis):", error)
    
    if platform.system() != 'Windows': 
        #os.system('cat IRT_param_freq.txt')
        os.system('cp IRT_param_freq.txt '+self.path_content+self.path_irt+self.path_dataset+self.bar+'IRT_param_freq_'+datasetName+'_'+model_name+'.txt')
    else:
        os.system('copy IRT_param_freq.txt '+self.path_content+self.path_irt+self.path_dataset+self.bar+'IRT_param_freq_'+datasetName+'_'+model_name+'.txt')
        #os.system('type IRT_param_freq.txt')
    return result_irt_new, result_irt
    
  def run_calc(self, name_of_features_x,datasetName,model_name):

    if self.exec_base_irt_score == self.exec_theta:
      url = self.path_content+self.path_irt+self.bar+'OutExecution'+self.bar+'theta_list.csv'
      name_col = 'Theta'
    else:
      if self.exec_base_irt_score == self.exec_trueScore:
        url = self.path_content+self.path_irt+self.bar+'OutExecution'+self.bar+'score_total.csv'
        name_col = 'Score'
    
    rank_theta = pd.read_csv(url)


    #if self.download_files:
    #  files.download(url)
    rank_theta = rank_theta.sort_values(name_col,ascending=True)
    
    # if exec_proposal == proposal_1_pool:
    #   k = number_of_features*number_of_features_deletion*4
    # else:
    #   if exec_proposal == proposal_2_loop:
    #     k = number_of_features*len(exec_variation_method)*number_of_features_variation
    
    
    #rank_theta.plot.barh(x='Clf',y=name_col,figsize = (15,k),color='green')
    rank_theta = rank_theta.set_index(keys='Clf')

    if self.exec_proposal == self.proposal_2_loop:
      rank_theta_loop = rank_theta.sort_values(by=name_col, ascending=True)

      df_rank_final = pd.DataFrame(index=name_of_features_x, columns=[str('Final '+name_col)])
      
      for _, feature in enumerate(name_of_features_x):
        if self.exec_calc_theta == self.theta_sum:
          df_rank_final.loc[feature,str('Final '+name_col)] = sum(rank_theta_loop.filter(like='"'+feature+'"', axis='index')[name_col])
        else:
          if self.exec_calc_theta == self.theta_min:
            df_rank_final.loc[feature,str('Final '+name_col)] = min(rank_theta_loop.filter(like='"'+feature+'"', axis='index')[name_col])
          else:
            if self.exec_calc_theta == self.theta_mean:
              df_rank_final.loc[feature,str('Final '+name_col)] = statistics.mean(rank_theta_loop.filter(like='"'+feature+'"', axis='index')[name_col])

      df_rank_final = df_rank_final.sort_values(by=str('Final '+name_col), ascending=True)
      df_rank_final
    else:
      if self.exec_proposal == self.proposal_1_pool:

        rank_theta_pool = rank_theta.sort_values(by=name_col, ascending=True)

        df_rank_final = pd.DataFrame(index=name_of_features_x, columns=[str('Final '+name_col)])
        
        for _, feature in enumerate(name_of_features_x):
          if self.exec_calc_theta == self.theta_sum:
            df_rank_final.loc[feature,str('Final '+name_col)] = sum(rank_theta_pool.filter(like=feature, axis='index')[name_col])
          else:
            if self.exec_calc_theta == self.theta_min:
              df_rank_final.loc[feature,str('Final '+name_col)] = min(rank_theta_pool.filter(like=feature, axis='index')[name_col])
            else:
              if self.exec_calc_theta == self.theta_mean:
                df_rank_final.loc[feature,str('Final '+name_col)] = statistics.mean(rank_theta_pool.filter(like=feature, axis='index')[name_col])

        df_rank_final = df_rank_final.sort_values(by=str('Final '+name_col), ascending=True)


    
    df_rank_final.to_csv(self.path_content+self.path_irt+self.path_dataset+self.bar+'rank_final_'+datasetName+'_'+model_name+'.csv',index=True)
    return df_rank_final

  def explainRankByEXirt(self, model, X_train, X_test, y_train, y_test,datasetName,model_name=''):

    self.path_dataset = self.bar+datasetName
    self.dirByDataset(self.path_dataset)

    if(self.exec_in == self.exec_test):
      data_exec_x = X_test
      data_exec_y = y_test 
    else:
      data_exec_x = X_train
      data_exec_y = y_train

    
    N = 500
    if len(data_exec_y) > N:
      data_sample = data_exec_x
      data_sample['class'] = data_exec_y

      #stratifier sampler
      data_sample = data_sample.groupby('class', group_keys=False).apply(lambda x: x.sample(int(np.rint(N*len(x)/len(data_sample))))).sample(frac=1).reset_index(drop=True)
      
      data_exec_y = data_sample['class']
      data_sample = data_sample.drop(labels='class', axis=1)
      data_exec_x = data_sample

    a, b = self.run_prepare(model, data_exec_x, data_exec_y, X_train, X_test, y_train, y_test,model_name)
    
    rirt_new, rirt = self.run_irt(datasetName,model_name)
    
    rank = self.run_calc(X_train.columns,datasetName,model_name)
    
    return list(rank.index), rank


  

def normalize(df):
    # copy the dataframe
    df_norm = df.copy()
    # apply min-max scaling
    for column in df_norm.columns:
        if(len(df_norm[column].unique()) > 1): #fix NaN generation
          df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())
        else:
          df_norm[column] = 0
    return df_norm

def main():
    
    dataset_name = "Australian"
    #load dataset by OpenML

    dataset = openml.datasets.get_dataset(dataset_name)
    X, Y, categorical_indicator, attribute_names = dataset.get_data(
                      dataset_format="dataframe", target=dataset.default_target_attribute)
    
    
    #Preprocess Y and X numerics
    #print(Y)
    
    if (Y.dtype != 'numeric'):
      Y = Y.astype(int)
    
    for i,c in enumerate(X.columns):
      if (X[c].dtype != 'float64'):
        X = X.astype(float)
    
    #Normalization
    X = normalize(X)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, stratify=Y) # 70% training and 30% test
    
    
    #Prediction model
    model = RandomForestClassifier(100,verbose=0)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    
    #Time meansure
    ini = time.time()
    explainer = Explainer()
    global_explanation_attributes, global_explanation_attributes_scores = explainer.explainRankByEXirt(model, X_train, X_test, y_train, y_test,dataset_name,model_name='m2')
    fim = time.time()
    print("Execution of eXirt in ms: ", fim-ini)
    
    print('This is a global rank of feature relevance by: '+ dataset_name)
    print(global_explanation_attributes_scores)
    print('Note: the attributes at the top of the rank are the most relevant to explain the model.')
    
if __name__ == "__main__":
    main()



