import numpy as np
import matplotlib.pyplot as plt

def show_mask(mask, ax, random_color=False):
    """
    mask: torch.tensor
    ax: plt

    """
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

def show_mask_image(mask, image, title=None, file_name=None):
    """
    mask: torch.tensor
    image: plt.Image
    title(optional): str
    file_name(optional): str. if not be identified, it will be nothing.

    return plt.gca()
    """

    plt.figure(figsize=(10,10))
    plt.imshow(image)
    show_mask(mask.cpu(), plt.gca())
    plt.axis('off')
    if title:
        plt.title(title, fontsize=18)
    if file_name:
        plt.savefig(file_name)
    plt.close()
    return plt.gca()