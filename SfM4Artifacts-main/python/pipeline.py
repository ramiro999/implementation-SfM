import os
from featmatch import FeatMatch
from sfm import SFM

class PiplineInit():
    def __init__(self, images, output, features, matcher, cross_check, save_results, calibration_mat, plot_error, pnp_prob, pnp_method, reprojection_thresh):
        self.images = images
        self.output = output
        self.ext = ['jpg', 'png']
        self.print_every = 1
        self.features = features
        self.matcher = matcher
        self.cross_check = cross_check
        self.save_results = save_results
        self.calibration_mat = calibration_mat
        self.plot_error = plot_error
        self.pnp_prob = pnp_prob
        self.pnp_method = pnp_method
        self.reprojection_thresh = reprojection_thresh

    def init_feature_matching(self):

        self._setup_feat_dirs()
        opts = dict({'data_dir': self.images, 'ext':self.ext, 'out_dir': self.output, 
                 'features':self.features, 'matcher':self.matcher, 'cross_check':self.cross_check, 
                 'print_every':self.print_every, 'save_results':self.save_results})
        return opts
    
    def init_sfm_reconstruction(self):
        self._setup_sfm_dirs()
        feat_dir = os.path.join(self.output, 'features', self.features)
        matches_dir = os.path.join(self.output, 'matches', self.matcher)
        out_cloud_dir = os.path.join(self.output, 'output_pcd', 'point-clouds')
        out_err_dir = os.path.join(self.output, 'output_pcd', 'errors')

        opts = dict({'images_dir':self.images, 'feat_dir':feat_dir, 'matches_dir':matches_dir, 
                 'out_cloud_dir':out_cloud_dir, 'out_err_dir':out_err_dir, 'plot_error':self.plot_error,
                   'cross_check':self.cross_check, 'matcher':self.matcher, 'calibration_mat':self.calibration_mat, 'pnp_prob':self.pnp_prob,
                     'pnp_method':self.pnp_method, 'reprojection_thresh':self.reprojection_thresh})
        return opts
    
    def _setup_feat_dirs(self):
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        if not os.path.exists(os.path.join(self.output, 'features')):
            os.makedirs(os.path.join(self.output, 'features'))

        if not os.path.exists(os.path.join(self.output, 'matches')):
            os.makedirs(os.path.join(self.output, 'matches'))

        if not os.path.exists(os.path.join(self.output, 'output_pcd')):
            os.makedirs(os.path.join(self.output, 'output_pcd'))

    def _setup_sfm_dirs(self):
        if not os.path.exists(os.path.join(self.output, 'output_pcd', 'point-clouds')):
            os.makedirs(os.path.join(self.output, 'output_pcd', 'point-clouds'))

        if not os.path.exists(os.path.join(self.output, 'output_pcd', 'errors')):
            os.makedirs(os.path.join(self.output, 'output_pcd', 'errors'))
        

if __name__ ==  "__main__":
    # Load Data
    images_dir = './datasets/caracalla/'
    output = './datasets/outputs/caracalla/'

    features = 'SIFT'
    matcher = 'FlannBasedMatcher'
    cross_check = False
    save_results = False

    plot_error = True
    # Load "default" for included dataset
    calibration_mat = 'default'

    pnp_prob = 0.80
    pnp_method = 'SOLVEPNP_ITERATIVE'
    reprojection_thresh = 8.0

    data_files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith('.jpg') or f.endswith('.png')]

   # Run the pipeline
    # Feature Matching 
    sfm = PiplineInit(images_dir, output, features, matcher, cross_check, save_results, calibration_mat, plot_error, pnp_prob, pnp_method, reprojection_thresh)
    feat_match_obj = sfm.init_feature_matching()
    FM = FeatMatch(feat_match_obj, data_files)
    # SfM Reconstruction 
    sfm_reconstruction_obj = sfm.init_sfm_reconstruction()
    SfM = SFM(sfm_reconstruction_obj)
    SfM.Run()


   