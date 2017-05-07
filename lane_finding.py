global int counter

 

## New = gamma * New + (1-gamma) * Old. 0 < gamma < 1.0

class Line():

    def __init__(self):

        # was line detected in the last iteration?

        self.detected = False 

        self.recent_leftx = []
        self.recent_lefty = []
        self.recent_rightx = []
        self.recent_righty = []
        self.history_leftx = []
        self.history_lefty = []
        self.history_rightx = []
        self.history_righty = []
        self.right_radius = None
        self.left_radius = None
        self.left_fit = None
        self.right_fit = None
        self.smooth_factor = 15

        self.xm_per_pix = 4/700
        self.ym_per_pix = 25/720

        #radius of curvature of the line in m 
        self.radius_of_curvature =  None
        self.radius_history = []
        #car pos from center of lane in m
        self.center_pos =  None

def main(self, warped):

    if find_lanes(self, warped) == True:

       calc_radius(self)

       if sanity_check(self) == True:

          self.history_leftx.append(self.recent_leftx)
          self.history_lefty.append(self.recent_lefty)
          self.history_rightx.append(self.recent_rightx)
          self.history_righty.append(self.recent_righty)
        
          # Fit a second order polynomial to each
          self.left_fit = np.polyfit(self.history_lefty[-self.smooth_factor:], self.history_leftx[-self.smooth_factor:], 2)
          self.right_fit = np.polyfit(self.history_righty[-self.smooth_factor:], self.history_rightx[-self.smooth_factor:], 2)           
          
          radius = (self.radius_left + self.radius_right)/2
          self.radius_history.append(radius)
          self.radius_of_curvature = np.average(self.radius_history[-self.smooth_factor:])

          self.center_pos = calc_car_pos(self,warped)

       elif left_fit==None or right_fit==None:

          self.history_leftx.append(self.recent_leftx)
          self.history_lefty.append(self.recent_lefty)
          self.history_rightx.append(self.recent_rightx)
          self.history_righty.append(self.recent_righty)
        
          # Fit a second order polynomial to each
          self.left_fit = np.polyfit(self.history_lefty[-self.smooth_factor:], self.history_leftx[-self.smooth_factor:], 2)
          self.right_fit = np.polyfit(self.history_righty[-self.smooth_factor:], self.history_rightx[-self.smooth_factor:], 2)           


def calc_radius(self):

    y_eval = 600
    #y_eval = np.max(ploty)

    # Fit new polynomials to x,y in world space
    left_fit_cr = np.polyfit(self.recent_lefty*self.ym_per_pix, self.recent_leftx*self.xm_per_pix, 2)
    right_fit_cr = np.polyfit(self.recent_righty*self.ym_per_pix, self.recent_rightx*self.xm_per_pix, 2)
    # Calculate the new radius of curvature
    self.left_radius = ((1 + (2*left_fit_cr[0]*y_eval*self.ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
    self.right_radius = ((1 + (2*right_fit_cr[0]*y_eval*self.ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
    # Now our radius of curvature is in meters        
    return True

def calc_car_pos(self,warped):

        ploty = np.linspace(0, warped.shape[0]-1, warped.shape[0] )
        left_fitx = self.left_fit[0]*ploty**2 + self.left_fit[1]*ploty + self.left_fit[2]
        right_fitx = self.right_fit[0]*ploty**2 + self.right_fit[1]*ploty + self.right_fit[2]
        #calculate offset of car from center of the road
        lane_center = (left_fitx[-1] + right_fitx[-1])/2
        car_center = warped.shape[1]/2
        center_diff = (car_center-lane_center)*self.xm_per_pix
        #side_pos = 'right'
        #if center_diff <= 0:
        #   side_pos = 'left'
        return center_diff 

def sanity_check(self):
    self.detected = False

    if (200 < self.left_fitx[-1] < 400) & (900 < self.right_fitx[-1] < 1100):

       self.detected = True

       if self.left_radius < 2000 or right_radius < 2000:

          check_radius = self.right_radius/self.left_radius

          if check_radius<0.5 or check_radius>1.5:
             self.detected = False

    return self.detected
 

def find_lanes(self, warped):

        # Take a histogram of the bottom half of the image

        histogram = np.sum(warped[int(warped.shape[0]/2):,:], axis=0)

        # Create an output image to draw on and  visualize the result

        out_img = np.dstack((warped, warped, warped))*255

 

        # Find the peak of the left and right halves of the histogram

        # These will be the starting point for the left and right lines

        midpoint = np.int(histogram.shape[0]/2)

        leftx_base = np.argmax(histogram[:midpoint])

        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

 

        # Choose the number of sliding windows

        nwindows = 9

        # Set height of windows

        window_height = np.int(warped.shape[0]/nwindows)

        # Identify the x and y positions of all nonzero pixels in the image

        nonzero = warped.nonzero()

        nonzeroy = np.array(nonzero[0])

        nonzerox = np.array(nonzero[1])

        # Current positions to be updated for each window

        leftx_current = leftx_base

        rightx_current = rightx_base

        # Set the width of the windows +/- margin

        margin = 100

        # Set minimum number of pixels found to recenter window

        minpix = 50

        # Create empty lists to receive left and right lane pixel indices

        left_lane_inds = []

        right_lane_inds = []

 

        # Step through the windows one by one

        for window in range(nwindows):

           # Identify window boundaries in x and y (and right and left)

           win_y_low = warped.shape[0] - (window+1)*window_height

           win_y_high = warped.shape[0] - window*window_height

           win_xleft_low = leftx_current - margin

           win_xleft_high = leftx_current + margin

           win_xright_low = rightx_current - margin

           win_xright_high = rightx_current + margin

           # Draw the windows on the visualization image

           cv2.rectangle(out_img,(int(win_xleft_low),int(win_y_low)),(int(win_xleft_high),int(win_y_high)),(0,255,0), 2)

           cv2.rectangle(out_img,(int(win_xright_low),int(win_y_low)),(int(win_xright_high),int(win_y_high)),(0,255,0), 2)

           # Identify the nonzero pixels in x and y within the window

           good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]

           good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]

           # Append these indices to the lists

           left_lane_inds.append(good_left_inds)

           right_lane_inds.append(good_right_inds)

           # If you found > minpix pixels, recenter next window on their mean position

           if len(good_left_inds) > minpix:

              leftx_current = np.int(np.mean(nonzerox[good_left_inds]))

           if len(good_right_inds) > minpix:       

              rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

 

        # Concatenate the arrays of indices

        left_lane_inds = np.concatenate(left_lane_inds)

        right_lane_inds = np.concatenate(right_lane_inds)

 

        # Extract left and right line pixel positions

        self.recent_leftx = nonzerox[left_lane_inds]

        self.recent_lefty = nonzeroy[left_lane_inds]

        self.recent_rightx = nonzerox[right_lane_inds]

        self.recent_righty = nonzeroy[right_lane_inds]

 

        # Fit a second order polynomial to each

        #left_fit = np.polyfit(lefty, leftx, 2)

        #right_fit = np.polyfit(righty, rightx, 2)           

        #return left_fit, right_fit
        return True 

                                                              

#if counter false detections >10:

#--- > search from scratch:

#else: search using last windows:

#             return leftx, lefty, rightx, righty

                              

Do Sanity check:

 

if False take Last Best fit, last center pos and last best Curvature,

                else WEIGHTED AVERAGE OVER CURRENT AND LAST FITS, CURVATURES (take middle of left and right) and center_pos

 

def sanity_check:

 

                self.detected = Faulse

 

  1.) curvatures similar

  2.) intercepts in range +- 100 px

  3.) (if detected/last_detected = True: xvalues from polyfit at y=0 and ymax similar (+-25px max) 

 

                if 1.)2.)3.)= TRUE: then self.detected = TRUE and SET COUNTER TO ZERO!

                ELSE counter += 1

               

                return self.detected