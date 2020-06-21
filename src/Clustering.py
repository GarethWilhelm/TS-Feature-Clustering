# Alternative methods

from sklearn.cluster import DBSCAN 
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA 
# Scaling the data to bring all the attributes to a comparable level 
scaler = StandardScaler() 
X_scaled = scaler.fit_transform(df.values) 
# Normalizing the data so that 
# the data approximately follows a Gaussian distribution 
# X_normalized = normalize(X_scaled) 
# Converting the numpy array into a pandas DataFrame 
X_normalized = pd.DataFrame(X_scaled)

pca = PCA(n_components = 2) 
X_principal = pca.fit_transform(X_normalized) 
X_principal = pd.DataFrame(X_principal) 
X_principal.columns = ['P1', 'P2'] 
print(X_principal.head())

# Numpy array of all the cluster labels assigned to each data point 
db = DBSCAN(eps = 0.0375, min_samples = 7).fit(X_principal) 
labels = db.labels_ 
print(np.unique(labels))
# # Building the label to colour mapping 
colours = {} 
colours[0] = 'r'
colours[1] = 'g'
colours[2] = 'b'
colours[3] = 'c'
colours[-1] = 'k'

# # Building the colour vector for each data point 
cvec = [colours[label] for label in labels]
colors = ['r', 'g', 'b', 'c', 'k']

plt.figure(figsize =(9, 9)) 

# For the construction of the legend of the plot 
r = plt.scatter(X_principal['P1'], X_principal['P2'], 
                marker ='x', color = colors[0]) 
g = plt.scatter(X_principal['P1'], X_principal['P2'], 
                marker ='+', color = colors[1]) 
b = plt.scatter(X_principal['P1'], X_principal['P2'], 
                marker ='*', color = colors[2]) 
c = plt.scatter(X_principal['P1'], X_principal['P2'], 
                marker ='o', color = colors[3])
k = plt.scatter(X_principal['P1'], X_principal['P2'], 
                marker ='o', color = colors[4]) 

# Plotting P1 on the X-Axis and P2 on the Y-Axis 
# according to the colour vector defined
plt.scatter(X_principal['P1'], X_principal['P2'], c = cvec)
plt.legend(
    #(r, g, b, c, k),
           ('Label 0', 'Label 1', 'Label 2', 'Label 3', 'Label 4','Label 5'), 
           scatterpoints = 1 ,loc ='upper left',ncol = 3,fontsize = 8) 
plt.show() 