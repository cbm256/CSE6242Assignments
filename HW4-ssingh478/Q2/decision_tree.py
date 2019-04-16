from util import entropy, information_gain, partition_classes
import numpy as np 
import ast


class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        self.tree = {}
        #pass

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        counts=np.bincount(y)
        ind=np.argmin(counts)
        samp=[]
        samp=[X[i] for i in range(len(y)) if y[i]==ind and X[i] not in samp]
        xuniq=len(samp)
        if len(np.unique(y))==1:
            self.tree['split_attribute']='Null'
            self.tree['split_value']='Null'
            self.tree['left']=y
            self.tree['right']=y
        elif xuniq==1 or len(y)<10 or (y.count(1)/y.count(0))>=0.8 or (y.count(0)/y.count(1))>=0.8:
            self.tree['split_attribute']='Null'
            self.tree['split_value']='Null'
            if (y.count(1)>=y.count(0)):
                self.tree['left']=1
            else:
                self.tree['left']=0 
            self.tree['right']=self.tree['left']
        else:
            #X=np.array(X)
            m=int(sqrt(len(X[0])))
            np.random.choice(range(len(X[0])),size=m,replace=False)
            #X=np.array(X)
            IG_max=[]
            split_val_max=[]
            for i in range(m):
                split_values=list(set([X[j][i] for j in range(len(y))]))
                for j,split_uniques in enumerate(split_values):
                    (X_left, X_right, y_left, y_right)=partition_classes(X, y, i, split_uniques)
                    IG.append(information_gain(y, [y_left,y_right]))
                IG_max.append(max(IG))
                IG_index=np.argmax(IG)
                split_val_max.append(split_values[IG_index])
            if IG_max==0:
                self.tree['split_attribute']='Null'
                self.tree['split_value']='Null'
                if (y.count(1)>=y.count(0)):
                    self.tree['left']=1
                else:
                    self.tree['left']=0 
                self.tree['right']=self.tree['left']
            else:
                IG_max_index=np.argmax(IG_max)
                split_attribute=IG_max[IG_max_index]
                split_value=split_val_max[IG_max_index]
                (X_left, X_right, y_left, y_right)=partition_classes(X, y, split_attribute, split_value)
                self.tree={'split_attribute':split_attribute,'split_value':split_value}
                self.tree['left']=DecisionTree()
                self.tree['right']=DecisionTree()
                self.tree['left'].learn(X_left,y_left)
                self.tree['right'].learn(X_right,y_right)
            
        #return tree               

        #pass


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        if self.tree['split_value']=='Null':
            return self.tree['left']
        else:
            if record[self.tree['split_attribute']]<=self.tree['split_value']:
                self.tree['left'].classify(record)
            else:
                self.tree['right'].classify(record)


        #pass
