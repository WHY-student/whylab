import numpy as np
import warnings

import matplotlib.pyplot as plt
from torch import  Tensor

def is_posion_valid(width, height, position: np.ndarray) -> bool:
    """Judge whether the position is in image.

    Args:
        position (np.ndarray): The position to judge which last dim must
            be two and the format is [x, y].

    Returns:
        bool: Whether the position is in image.
    """
    flag = (position[..., 0] < width).all() and \
            (position[..., 0] >= 0).all() and \
            (position[..., 1] < height).all() and \
            (position[..., 1] >= 0).all()
    return flag

def visual_box(image_numpy, bboxes, scores=None, labels=None, pred_score_thr=0.5, output_file_path=None, rescale=False, 
               color="red", font_size=10):
    """Draw single or multiple bboxes.

    Args:
        image_numpy (np.ndarray): The image to draw.
        bboxes (Union[np.ndarray, torch.Tensor]): The bboxes to draw with
            the format of(x1,y1,x2,y2).
        bboxes (Union[np.ndarray, torch.Tensor]): The scores to draw with the bboxes.
        edge_colors (Union[str, tuple, List[str], List[tuple]]): The
            colors of bboxes. ``colors`` can have the same length with
            lines or just single value. If ``colors`` is single value, all
            the lines will have the same colors. Refer to `matplotlib.
            colors` for full list of formats that are accepted.
            Defaults to 'g'.
        line_styles (Union[str, List[str]]): The linestyle
            of lines. ``line_styles`` can have the same length with
            texts or just single value. If ``line_styles`` is single
            value, all the lines will have the same linestyle.
            Reference to
            https://matplotlib.org/stable/api/collections_api.html?highlight=collection#matplotlib.collections.AsteriskPolygonCollection.set_linestyle
            for more details. Defaults to '-'.
        line_widths (Union[Union[int, float], List[Union[int, float]]]):
            The linewidth of lines. ``line_widths`` can have
            the same length with lines or just single value.
            If ``line_widths`` is single value, all the lines will
            have the same linewidth. Defaults to 2.
        face_colors (Union[str, tuple, List[str], List[tuple]]):
            The face colors. Defaults to None.
        alpha (Union[int, float]): The transparency of bboxes.
            Defaults to 0.8.
    """
    if isinstance(bboxes, Tensor):
        bboxes = bboxes.cpu().numpy()

    width, height = image_numpy.shape[:2]

    if len(bboxes.shape) == 1:
        bboxes = bboxes[None]
    assert bboxes.shape[-1] == 4, (
        f'The shape of `bboxes` should be (N, 4), but got {bboxes.shape}')
    assert (bboxes[:, 0] <= bboxes[:, 2]).all() and (bboxes[:, 1] <=
                                                        bboxes[:, 3]).all()
    if not is_posion_valid(width, height, bboxes.reshape((-1, 2, 2))):
        warnings.warn(
            'Warning: The bbox is out of bounds,'
            ' the drawn bbox may not be in the image', UserWarning)
    
    # 初始化幕布
    plt.figure(figsize=(10,10))
    plt.imshow(image_numpy)
    ax = plt.gca()
    ax.axis('off')

    if scores is None:
        scores = [100] * len(labels)
    
    if labels is None:
        labels = ['target'] * len(scores)

    for bbox, score, label in zip(bboxes, scores, labels):
        if score < pred_score_thr:
            continue
        x0, y0, x1, y1 = bbox
        w, h = x1 - x0, y1 - y0
        # Display bbox
        ax.add_patch(
            plt.Rectangle(
                (x0, y0), w, h, edgecolor="red", facecolor=(0, 0, 0, 0), lw=2
            )
        )
        # Display score
        if score != 100:
            ax.text(x0, y0-2, f'{score:.2f}', fontsize=font_size, color=color)
        # Display label
        ax.text(x0 + 30 , y0-2, f'{label}', fontsize=font_size, color=color)


    if output_file_path is None:
        plt.savefig("result.jpg", bbox_inches='tight', pad_inches=0)
    else:
        plt.savefig(output_file_path, bbox_inches='tight', pad_inches=0)
    
    plt.close()


        
    # pred_instances = pred_instances[
    #     pred_instances.scores > pred_score_thr]

    


    # assert image is not None
    # image = image.astype('uint8')
    # self._image = image
    # self.width, self.height = image.shape[1], image.shape[0]
    # self._default_font_size = max(
    #     np.sqrt(self.height * self.width) // 90, 10)

    # # add a small 1e-2 to avoid precision lost due to matplotlib's
    # # truncation (https://github.com/matplotlib/matplotlib/issues/15363)
    # self.fig_save.set_size_inches(  # type: ignore
    #     (self.width + 1e-2) / self.dpi, (self.height + 1e-2) / self.dpi)
    # # self.canvas = mpl.backends.backend_cairo.FigureCanvasCairo(fig)
    # self.ax_save.cla()
    # self.ax_save.axis(False)
    # self.ax_save.imshow(
    #     image,
    #     extent=(0, self.width, self.height, 0),
    #     interpolation='none')

if __name__ == "__main__":
    # Example usage:
    image_numpy = np.random.rand(100, 100, 3)  # Example image, replace with your image data
    bboxes = np.array([[20, 30, 80, 70]])  # Example bounding boxes, replace with your bbox data
    scores = np.array([0.8])  # Example scores, replace with your score data
    labels = np.array([1])  # Example labels, replace with your label data
    visual_box(image_numpy, bboxes, scores, labels)

