import torch
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

# pip install scikit-learn

def visual_tsne(input_tensor, labels=None, save_file_path=None):
    """Draw tsne visual of tensor

    Args:
        input_tensor(torch.tensor): (num_class, num_token, channel), 
            num_class: The number of clusters you want to display,
            num_token: the number of token in each cluster,
            channel: the dim.
        save_file_path(str): the path of plt save
    Returns:
        None
    """
    if input_tensor is None:
        # 假设你的张量是这个
        input_tensor = torch.randn(8, 20, 512)  # 示例数据
    num_class, num_token, c = input_tensor.shape

    # 将张量重新整理成 (8*20, 512) 的形状
    data = input_tensor.view(-1, c).numpy()  # 转换为 NumPy 数组

    if labels is None:
        # 创建标签
        labels = np.repeat(np.arange(num_class), num_token)  # 标签 [0,0,...,1,1,...,7,7,...] 共 160 个标签
    else:
        labels = np.repeat(labels, num_token)

    # 应用 t-SNE 降维
    tsne = TSNE(n_components=2, random_state=42)
    reduced_data = tsne.fit_transform(data)

    # 创建一个 DataFrame 以方便绘图
    import pandas as pd
    df = pd.DataFrame(reduced_data, columns=['Dimension 1', 'Dimension 2'])
    df['Label'] = labels

    # 使用 seaborn 绘图
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='Dimension 1', y='Dimension 2', hue='Label', palette='tab10', alpha=0.7)
    plt.title('t-SNE Visualization of Tensor Data')
    plt.legend(title='Label')
    if save_file_path is None:
        plt.savefig("result.png")
    else:
        plt.savefig(save_file_path)