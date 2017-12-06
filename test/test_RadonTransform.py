import os
import numpy as np
import cv2
from tqdm import tqdm

import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.transform import radon, iradon
from radon_transform import generateRadonLines, findCrossPoint


                            
#root = 'C:/Users/chulh/문서/Git/avm_dataset/test/'
root = 'C:/Users/chulh/문서/Git/avm_dataset/dataset/hyu_171025/rectified/set1/output/labeled/class_1'
output_dir = 'C:/Users/chulh/Documents/output'

f0 = 146
f1 = 1300

log_ang = []
for i in tqdm(range(f0,f1)):        
    img_file = os.path.join(root, '{:08d}.jpg'.format(i))
    img = imread(img_file, as_grey=True)
    img = cv2.resize(img, None, fx=0.25, fy=0.25)
    
    # rdaon transform
    prj_t = radon(img)
    center = prj_t.shape[0] // 2
    offset, ang_ps1 = np.unravel_index(prj_t.argmax(), prj_t.shape) # ang_ps1: radon image domain
    log_ang.append(ang_ps1)
    
    # line generation for principle angle 1
    lines_ps1 = generateRadonLines(prj_t, ang_ps1, 0.5, 20, center, (img.shape[1], img.shape[0]))
    
    # line generation for principle angle 2
    ang_ps2 = 0
    if ang_ps1 < 90:
        ang_ps2 = 90 + ang_ps1
    elif ang_ps1 > 90:
        ang_ps2 = ang_ps1 - 90
    elif ang_ps1 == 90:
        ang_ps2 = 0
        
    lines_ps2 = generateRadonLines(prj_t, ang_ps2, 0.5, 20, center, (img.shape[1], img.shape[0]))
    
    # cross point
    pts = []
    for l1 in lines_ps1:    
        for l2 in lines_ps2:
            x, y = findCrossPoint((l1.get_a(), l1.get_b()), (l2.get_a(), l2.get_b()))
            pts.append((x,y))
            
    # draw
    img_debug = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    for l in lines_ps1:
        img_debug = cv2.line(img_debug, (np.int(l.end_pts[0][0]), np.int(l.end_pts[0][1])),
                            (np.int(l.end_pts[1][0]), np.int(l.end_pts[1][1])), (255,0,0), 1)
        
    for l in lines_ps2:
        img_debug = cv2.line(img_debug, (np.int(l.end_pts[0][0]), np.int(l.end_pts[0][1])),
                            (np.int(l.end_pts[1][0]), np.int(l.end_pts[1][1])), (0,0,255), 1)
    for pt in pts:
        img_debug = cv2.circle(img_debug, (np.int(pt[0]), np.int(pt[1])), 1, (255,255,0), 1)
    
    save_file = os.path.join(output_dir, '{:08d}.png'.format(i))    
    cv2.imwrite(save_file, img_debug)
        



'''
plt.plot(prj_ps1)
plt.show()


iteration = 10
sum_time = 0
for i in range(iteration):
    start_time  = time.time()
    prj_t = radon(img)
    sum_time += time.time() - start_time
avg_time = sum_time / iteration
print("avg time [radon]: {} ms".format(avg_time * 1000))
'''

'''
iteration = 1
sum_time = 0
for i in range(iteration):
    start_time  = time.time()
    indexes = peakutils.indexes(prj_ps1.reshape(prj_ps1.shape[0],), thres=0.02/max(prj_ps1), min_dist=20) # 3.3ms
    sum_time += time.time() - start_time
avg_time = sum_time / iteration
print("avg time [peak detection]: {} ms".format(avg_time * 1000))
'''


