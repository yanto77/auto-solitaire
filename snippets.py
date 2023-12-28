

def load_and_match():
    import cv2
    import pyscreeze
    from matplotlib import pyplot as plt

    screen = pyscreeze._load_cv2('foo.png', grayscale=False)
    # delta = 20
    # region = pyscreeze.Box(left=2695-delta, top=551-delta, width=20+delta*2, height=20+delta*2)
    # screen = screen[region[1] : region[1] + region[3], region[0] : region[0] + region[2]]

    # plt.imshow(screen, interpolation='nearest')
    # plt.savefig('bar0.png')

    # NB: grayscale defaults to None, which is converted to True. Red/black values 
    # are very similar in grayscale, so we have to be careful here to always 
    # remember grayscale=False.
    im1 = pyscreeze._load_cv2('img/black10.png', grayscale=False)
    im2 = pyscreeze._load_cv2('img/red10.png', grayscale=False)
    im3 = cv2.imread('img/black10.png', cv2.IMREAD_COLOR)
    im4 = cv2.imread('img/red10.png', cv2.IMREAD_COLOR)

    for (idx, im) in enumerate([im1, im2, im3, im4]):
        result = cv2.matchTemplate(screen, im, cv2.TM_CCOEFF_NORMED)

        plt.imshow(result, interpolation='nearest')
        plt.savefig('bar{}.png'.format(idx))

        plt.imshow(im, interpolation='nearest')
        plt.savefig('bar{}_im.png'.format(idx))
