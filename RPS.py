# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[]):
  import pandas as pd
  from statsmodels.tsa.deterministic import Fourier
  from statsmodels.tsa.deterministic import DeterministicProcess
  from sklearn.linear_model import LinearRegression
  
  if prev_play=="":
    return random_RPS()

  else:
    
    opponent_history.append(prev_play)

    if len(opponent_history)>4:

      sh=pd.DataFrame(opponent_history,columns =['CH'])
      # ignore the none value for the first prev_play
      dh = sh.dropna(axis=0)
      # print(oh.head())

      lst = [ {"R":0,"P":1,"S":-1},{"R":0,"P":-1,"S":1},{"R":1,"P":0,"S":-1},{"R":1,"P":-1,"S":0},{"R":-1,"P":1,"S":0},{"R":-1,"P":0,"S":1}]
      win_pair = {"P":"S","R":"P","S":"R"}

      precision = 0
      v=0
      
      for item in lst:
        oh=dh.tail(5).copy()
        oh['CH'] = oh.CH.map(item)
        y = oh['CH']
        # print(y.head())

        fourier_gen = Fourier(3, order=1)

        dp = DeterministicProcess(
            index=y.index,
            period=3,
            # constant=True,
            order=1,
            # order=2, 降低准确率
            seasonal=True,               
            additional_terms=[fourier_gen], 
            # drop=True,
        )

        X = dp.in_sample()

        model = LinearRegression().fit(X, y)

        y_original = y.to_numpy()
        # print("y_original:",y_original)
        y_predict_temp = model.predict(X)
        y_predict=[round(i) for i in y_predict_temp]
        # print("y_predict:",y_predict)        

        sl=similar(y_original,y_predict)
        # print("sl:",sl)

        if sl>precision:
          precision=sl
          X_fore = dp.out_of_sample(steps=1)
          # print("X_force:",X_fore)
          y_fore = model.predict(X_fore)
          # print("y_force:",y_fore)
          v=round(y_fore[0])
          if v in [0,1,-1]:
            RPS=[k for k,l in item.items() if l==v][0]
            return win_pair[RPS]
      # 找到问题了，首先预测值输出不对，其次预测值只是接近0,1，-1，但是不是0,1，-1本身，需要写一个函数，根据也测结果，输出选择
      # 距离哪个近取哪个值
      # if (abs(v)<abs(v-1))&(abs(v)<abs(v+1)):
      #   # print("P") # always output P
      #   return "P"
      # elif (abs(v-1)<abs(v))&(abs(v-1)<abs(v+1)):

      #   # print("S")
      #   return "S"
      # elif (abs(v+1)<abs(v))&(abs(v+1)<abs(v-1)):
      #   # print("R")
      #   return "R"    
      # else:              
      #   return random_RPS()

    else:
      return random_RPS()

def random_RPS():
  import random
  a = ["R","P","S"]
  b = random.sample(a, 1)
  return b[0]

def similar(a,b):
  j=0
  for i in range(len(a)):
    if a[i]==int(b[i]):
      j=j+1
  return j