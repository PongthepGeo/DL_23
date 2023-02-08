#-----------------------------------------------------------------------------------------#
import sys
sys.path.append('./Libs') 
import utilities as U
import neural_network_architectures as NNA
#-----------------------------------------------------------------------------------------#
import torch
import matplotlib.pyplot as plt
import torch.utils.data as data
#-----------------------------------------------------------------------------------------#
from torchvision import datasets, transforms
from tqdm import tqdm
#-----------------------------------------------------------------------------------------#
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using PyTorch version:', torch.__version__, ' Device:', device)
#-----------------------------------------------------------------------------------------#

# NOTE predifined parameters
download_folder = '../larger_than_50_MB/'
batch_size = 128 # depends on GPU memory size
image_dim_1 = 28; image_dim_2 = 28
output_dim = 10 # should equal to number of classes
save_model = '../larger_than_50_MB/save_trained_model/MLP.pt'
number_of_images = 10000

'''
step 1: manipulate data. We re-download MNIST dataset and batch dataset to fit CPU capacities.
'''

# NOTE training data
train_transforms = transforms.Compose([transforms.ToTensor()])
train_data = datasets.MNIST(root=download_folder,
							train=True,
							download=True,
							transform=train_transforms)
train_iterator = data.DataLoader(train_data, shuffle=True, batch_size=batch_size)

'''
step 2: select neural networks for applying T-distributed Stochastic Neighbor Embedding (tSNE).
'''

# model = NNA.MLP((image_dim_1 * image_dim_2), output_dim)
model = NNA.LeNet(output_dim)
model = model.to(device)
model.load_state_dict(torch.load(save_model))
outputs, intermediates, labels = U.get_representations(model,
													 train_iterator,
													 device)

'''
step 3: fit some images to the inference. Selected neural layers (inference) will use to predict the input images and those images require high flatting dimensions into 2D before fitting the inference. The result shows MNISTs' clusters based on tSNE computation.  
'''

intermediate_tsne_data = U.get_tsne(intermediates, n_images=number_of_images)
U.plot_representations(intermediate_tsne_data, labels, n_images=number_of_images)