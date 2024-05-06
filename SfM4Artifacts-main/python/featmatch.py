import cv2 
import numpy as np 
import pickle 
import os 
from time import time
from utils import * 

class FeatMatch:
    def __init__(self, opts, data_files=[]):
        self.opts = opts
        self.data_files = data_files

        if len(self.data_files) == 0: 
            self.img_names = sorted(os.listdir(self.opts['data_dir']))
            self.img_paths = [os.path.join(self.opts['data_dir'], x) for x in self.img_names if \
                        x.split('.')[-1] in self.opts['ext']]
        
        else: 
            self.img_paths = self.data_files
            self.img_names = sorted([x.split('/')[-1] for x in self.data_files])
            
        self.feat_out_dir = os.path.join(self.opts['out_dir'],'features',self.opts['features'])
        self.matches_out_dir = os.path.join(self.opts['out_dir'],'matches',self.opts['matcher'])

        if not os.path.exists(self.feat_out_dir): 
            os.makedirs(self.feat_out_dir)
        if not os.path.exists(self.matches_out_dir): 
            os.makedirs(self.matches_out_dir)
        
        self.data = []
        self.t1 = time()
        for i, img_path in enumerate(self.img_paths): 
            img = cv2.imread(img_path)
            img_name = self.img_names[i].split('.')[0]
            img = img[:,:,::-1]
            # TODO: Change Feature Matcher and move to separate class
            feat = getattr(cv2.xfeatures2d, '{}_create'.format(self.opts['features']))()
            kp, desc = feat.detectAndCompute(img,None)
            self.data.append((img_name, kp, desc))

            kp_ = SerializeKeypoints(kp)
            
            with open(os.path.join(self.feat_out_dir, 'kp_{}.pkl'.format(img_name)),'wb') as out:
                pickle.dump(kp_, out)

            with open(os.path.join(self.feat_out_dir, 'desc_{}.pkl'.format(img_name)),'wb') as out:
                pickle.dump(desc, out)

            if self.opts['save_results']: 
                raise NotImplementedError

            self.t2 = time()

            if (i % self.opts['print_every']) == 0:    
                print('FEATURES DONE: {0}/{1} [time={2:.2f}s]'.format(i+1,len(self.img_paths),self.t2-self.t1))

            self.t1 = time()

        self.num_done = 0 
        self.num_matches = ((len(self.img_paths)-1) * (len(self.img_paths))) / 2

        self.t1 = time()
        for i in range(len(self.data)): 
            for j in range(i+1, len(self.data)): 
                img_name1, _, desc1 = self.data[i]
                img_name2, _, desc2 = self.data[j]

                if self.opts['matcher'] == 'BFMatcher':
                    matcher = cv2.BFMatcher_create()
                elif self.opts['matcher'] == 'FlannBasedMatcher':
                    matcher = cv2.FlannBasedMatcher_create()

                matches = matcher.match(desc1,desc2)
                matches = sorted(matches, key = lambda x:x.distance)
                matches_ = SerializeMatches(matches)

                pickle_path = os.path.join(self.matches_out_dir, 'match_{}_{}.pkl'.format(img_name1,
                                                                                     img_name2))
                with open(pickle_path,'wb') as out:
                    pickle.dump(matches_, out)

                self.num_done += 1 
                self.t2 = time()

                if (self.num_done % self.opts['print_every']) == 0: 
                    print('MATCHES DONE: {0}/{1} [time={2:.2f}s]'.format(self.num_done, self.num_matches, self.t2-self.t1))

                self.t1 = time()

if __name__=='__main__': 
    # Example usage
    data_dir = './datasets/boy_with_thorn/'
    data_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.jpg') or f.endswith('.png')]
    out_dir = './datasets/boy_with_thorn/outputs/'
    ext = ['jpg','png']
    features = 'SIFT'
    matcher = 'FlannBasedMatcher'
    cross_check = False
    print_every = 1
    save_results = False

    opts = dict({'data_dir':data_dir, 'ext':ext, 'out_dir':out_dir, 
                 'features':features, 'matcher':matcher, 'cross_check':cross_check, 
                 'print_every':print_every, 'save_results':save_results})

    feat_match = FeatMatch(opts, data_files)
